'use strict'
const fs = require('fs')
const nconf = require('./config/conf.js').nconf
const csv = require('csv-parser')


const filePath = nconf.get('inputFilePath')
const sourceSequenceLength = nconf.get('sourceSequenceLength')
const inputSequenceLength = nconf.get('inputSequenceLength')
const outputSequenceLength = nconf.get('outputSequenceLength')
const offset = nconf.get('offset')
const inputAttributes = nconf.get('inputAttributes')
const outputAttributes = nconf.get('outputAttributes')

let itemCount = 0
let inputItems = []
let outputItems = []

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
  		process.exit(1)
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
 
  });

  const processItems = (inputItems, outputItems) => {

  	const nIterations = (sourceSequenceLength - offset) - (inputSequenceLength + outputSequenceLength) + 1
  	//console.log(nIterations)
  	for(let i=0;i< nIterations; i++){
  		let inputSequence = []
  		let outputSequence = []
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
  		//console.log('outputSequence')
  		//console.log(outputSequence)

  		doSimulate(inputSequence, outputSequence)
  	}
  	
  }