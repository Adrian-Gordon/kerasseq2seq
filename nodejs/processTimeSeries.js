'use strict'
const fs = require('fs')
const nconf = require('./config/conf.js').nconf
const csv = require('csv-parser')
const request = require('request-promise')
const { Trader } = require('trader')


const filePath = nconf.get('inputFilePath')
const sourceSequenceLength = nconf.get('sourceSequenceLength')
const inputSequenceLength = nconf.get('inputSequenceLength')
const outputSequenceLength = nconf.get('outputSequenceLength')
const offset = nconf.get('offset')
const inputAttributes = nconf.get('inputAttributes')
const outputAttributes = nconf.get('outputAttributes')
const outputIndexes = nconf.get('outputIndexes')
const targetTicks = nconf.get('targetTicks')

let itemCount = 0
let inputItems = []
let outputItems = []

let sequences = []

const processFile = () => {


  fs.createReadStream(filePath)
    .pipe(csv())
    .on('data', (data) => {
    	itemCount++
    	if(itemCount > sourceSequenceLength){
    		//console.log("inputItems")
    		//console.log(inputItems)
    		//console.log("outputItems")
    		//console.log(outputItems)
    		processItems(inputItems, outputItems)
    		itemCount = 0
    		inputItems = []
    		outputItems = []
    		//process.exit(1)
    	}

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
    for(let i = 0; i < 20; i++){
      const is = sequences[i].inputSequence
      const os = sequences[i].outputSequence
      const rs = sequences[i].remainingSequence
      const response = await doSimulate(is)
      const predictions = response.body
      const lastObservations = is[inputSequenceLength -1]
      const lastPredictions = predictions[outputSequenceLength -1]
      console.log(lastObservations)
      console.log(lastPredictions)
    }
    

  }

  const doSimulate = (inputSequence) => {
    console.log("inputSequence")
    console.log(inputSequence)
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