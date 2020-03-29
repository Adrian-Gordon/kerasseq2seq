'use strict'
const fs = require('fs')
const nconf = require('./config/conf.js').nconf
const csv = require('csv-parser')
const request = require('request-promise')
const { Trader } = require('./trader.js')


const filePath = nconf.get('inputFilePath')
const sourceSequenceLength = nconf.get('sourceSequenceLength')
const inputSequenceLength = nconf.get('inputSequenceLength')
const outputSequenceLength = nconf.get('outputSequenceLength')
const offset = nconf.get('offset')
const inputAttributes = nconf.get('inputAttributes')
const outputAttributes = nconf.get('outputAttributes')
const outputIndexes = nconf.get('outputIndexes')
const targetTicks = nconf.get('targetTicks')
const stopLossTicks = nconf.get('stopLossTicks')
const maxPrice = nconf.get('maxPrice')

let itemCount = 0
let inputItems = []
let outputItems = []

let sequences = []
let inputSequencesCount = 0

const processFile = () => {


  fs.createReadStream(filePath)
    .pipe(csv())
    .on('data', (data) => {
    	itemCount++

      let inputItem = []
      for(let i=0;i<inputAttributes.length; i++){
        const value = data[inputAttributes[i]]
        inputItem.push(parseFloat(value))
      }
      inputItems.push(inputItem)

      let outputItem = []
      for(let i=0;i<outputAttributes.length; i++){
        const value = data[outputAttributes[i]]
        outputItem.push(parseFloat(value))
      }
      outputItems.push(outputItem)

    	if(itemCount >= sourceSequenceLength){
    		//console.log("inputItems" + inputItems.length)
        //console.log("outputItems" + outputItems.length)
    		//console.log(inputItems)
    		//console.log("outputItems")
    		//console.log(outputItems)
    		processItems(inputItems, outputItems)
        inputSequencesCount++
       /* if(inputSequencesCount > 2){
          for(let i=0;i<sequences.length;i++){
            console.log(sequences[i].inputSequence)
            console.log(sequences[i].outputSequence)
          }
          process.exit(0)
        }*/
    		itemCount = 0
    		inputItems = []
    		outputItems = []
    		//process.exit(1)
    	}

   

  	})
    .on('end', () => {
      processSequences()
   
    });
  }

  const processItems = (inputItems, outputItems) => {

  	const nIterations = (sourceSequenceLength - offset) - (inputSequenceLength + outputSequenceLength) + 1
  	//console.log(nIterations)
  	for(let i=0;i< nIterations; i++){
  		let inputSequence = []
  		let outputSequence = []
      let remainingSequence = []
  		const startIndex = offset + i
  		const inputEndIndex = startIndex + inputSequenceLength

  		for(let j = startIndex; j < inputEndIndex; j++){
  			inputSequence.push(inputItems[j])
  		}
  		//console.log("inputSequence")
  		//console.log(inputSequence)

  		for(let j = startIndex + inputSequenceLength; j < startIndex + inputSequenceLength + outputSequenceLength; j++){
  			outputSequence.push(outputItems[j])
  		}

      for(let j = startIndex + inputSequenceLength; j < sourceSequenceLength; j++){
        remainingSequence.push(outputItems[j])
      }
  		//console.log('outputSequence')
  		//console.log(outputSequence)

      const sequence = {
        'inputSequence': inputSequence,
        'outputSequence': outputSequence,
        'remainingSequence': remainingSequence
      }
      sequences.push(sequence)
  	  // doSimulate(inputSequence, outputSequence, remainingSequence)
  	}
  	
  }

  const processSequences = async () => {
    let layToBackReturns = 0.0
    let backToLayReturns = 0.0
    let backToLayBets = 0
    let layToBackBets = 0
    for(let i = 0; i < sequences.length; i++){
      const is = sequences[i].inputSequence
      if(is[0][0] > 0 && is[0][0] <= maxPrice){
          //console.log(is)
          const os = sequences[i].outputSequence
          //console.log(os)
          const rs = sequences[i].remainingSequence
          const rsLay = rs.map(obs => {
            return(obs[0])
          })
          const rsBack = rs.map(obs => {
            return(obs[1])
          })
          const response = await doPrediction(is)
          const predictions = response.body
          const lastObservations = is[inputSequenceLength -1]
          const lastObservedLayprice = lastObservations[outputIndexes[0]]
          const lastObservedBackPrice = lastObservations[outputIndexes[1]]
          const lastPredictions = predictions[outputSequenceLength -1]
          const lastPredictedLayprice = lastPredictions[0]
          const lastPredictedBackprice = lastPredictions[1]
    //      console.log(lastObservations)
    //      console.log(lastPredictions)
    //      console.log(lastObservedLayprice + " " + lastObservedBackPrice, + " " + lastPredictedLayprice + " " + lastPredictedBackprice)
          if(lastObservedLayprice > 0.0){
              if(Trader.isTradingOpportunity(lastObservedBackPrice, lastPredictedLayprice, targetTicks )){
                //it's a back to lay opportunity
                console.log(i + "Back to lay Opportunity")
                console.log(lastObservedLayprice + " " + lastObservedBackPrice, + " " + lastPredictedLayprice + " " + lastPredictedBackprice)
                console.log(is)
                console.log(os)
                console.log(rs)
                console.log(rsLay)
                console.log(rsBack)
                console.log(predictions)
                const returns = Trader.simulateBackToLay(lastObservedBackPrice, 1.0, rsLay, targetTicks, stopLossTicks)
                console.log("Returns: " + JSON.stringify(returns))
                backToLayBets++
                backToLayReturns += returns.returns

              }
              else if(Trader.isTradingOpportunity(lastPredictedBackprice, lastObservedLayprice, targetTicks)){
                //it's a lay to back opportunity
                console.log(i + "Lay to back Opportunity")
                console.log(lastObservedLayprice + " " + lastObservedBackPrice, + " " + lastPredictedLayprice + " " + lastPredictedBackprice)
                console.log(is)
                console.log(os)
                console.log(rs)
                console.log(rsLay)
                console.log(rsBack)
                console.log(predictions)
                const returns = Trader.simulateLayToBack(lastObservedLayprice, 1.0, rsBack, targetTicks, stopLossTicks)
                console.log("Returns: " + JSON.stringify(returns))
                layToBackBets++
                layToBackReturns += returns.returns
                console.log("layToBackReturns: " + layToBackReturns + "(" + layToBackBets + ")")
                //process.exit(1)
              }
              else {
                //console.log("No trade")
              }
            }
        }
    }
    console.log("layToBackReturns: " + layToBackReturns + "(" + layToBackBets + ")")
    console.log("backToLayReturns: " + backToLayReturns + "(" + backToLayBets + ")")
    

  }

  const doPrediction = (inputSequence) => {
 //   console.log("inputSequence")
 //   console.log(inputSequence)
   /* console.log("outputSequence")
    console.log(outputSequence)
    console.log("remainingSequence")
    console.log(remainingSequence)*/
    const options = {
      headers: { 'Content-Type': 'application/json' },
      uri: nconf.get('inferenceServiceUri'),
      body: inputSequence, 
      resolveWithFullResponse: true,
      simple: false,
      json: true,
    }
    //console.log(options)
    return request.post(options)
 

  }


  processFile()