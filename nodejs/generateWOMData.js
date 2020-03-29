const ticksLookup=[
  [2.0, 100, 100, 0.02],
  [3.0, 50, 150, 0.05],
  [4.0, 20, 170, 0.1],
  [6.0, 20, 190, 0.2],
  [10.0, 20, 210, 0.5],
  [20.0, 20, 230, 1.0],
  [30.0,10, 240, 2.0],
  [50.0, 10, 250, 5.0]
  ]
 
const quotient = 0.01

const getTicksFromPrice = (price) => {
let ticks = 0
let index = -1
for(let i = 0; i < 8; i++){
    //console.log(price + " " + ticksLookup[i][0])
    if(price >= ticksLookup[i][0]){
        index++
    }
    else {
        //console.log(index)
        if(index == -1) break
        ticks = ticksLookup[index][2]
        let dif = price - ticksLookup[index][0]
        let difInTicks = dif / (ticksLookup[index][3])
        ticks += difInTicks
        break
    }

}
if(index == -1){
        ticks = (price - 1.0) / 0.01
}

return(Math.floor(ticks))
}
 
const getPriceFromTicks = (ticks) => {
try{
    for(let i = 0; i< 8; i ++){
        if(ticksLookup[i][2] >= ticks){
            if(i==0){
                            return(1.0 + (ticks * 0.01))
            }
            remainder = ticksLookup[i][2] - ticks
            //console.log(i + " " + remainder);
            const price = ticksLookup[i][0] - (remainder * ticksLookup[i -1 ][3])
            return(price)
            break;
        }
    }
}catch(err){
                console.log(err)
                console.log(ticks)
}
}
 

 


let runningCount = 1

 

let header="No,layprice1,backprice1,WOM"

/*for(let i=0;i<10;i++){

                header = header + "layprice" + (i+1) + "," + "laydepth" + (i+1) +","

}

//header = header + ","

for(let i=0;i<10;i++){

                header = header + "backprice" + (i+1) + "," + "backdepth" + (i+1)

                if(i< 9)

                                header=header + ","

}

*/

console.log(header)

 

 

const generateSequence = (inputSequenceLength, outputSequenceLength, runLength) => {

    const startPriceTicks1= 110 + (Math.floor(Math.random() * 90))
    const startPriceTicks2 = startPriceTicks1 -2
    //console.log(startPriceTicks1 + " " + startPriceTicks2)
    const startPrice1 = getPriceFromTicks(startPriceTicks1)
    const startPrice2 = getPriceFromTicks(startPriceTicks2)


    const runStartIndex = inputSequenceLength - Math.floor(Math.random() * runLength)

    //console.log(runStartIndex)

    let sequence = []


    for(let i=0;i< runStartIndex; i++){

        let ticks1 = startPriceTicks1

        let ticks2 = startPriceTicks2

        let record ={

                        "layprice1": getPriceFromTicks(ticks1).toFixed(2),

                        "backprice1": getPriceFromTicks(ticks2).toFixed(2),

                        "wom": 0.0

                       

        }

        sequence.push(record)

    }

    let ticks1 = startPriceTicks1

    let ticks2 = startPriceTicks2

    const wom = (2.0 * Math.random()) -1.0;

    const probdif = wom * quotient;

    let newPrice1

    let newPrice2

    let prob = 1.0 / getPriceFromTicks(ticks1)

    for(let i=runStartIndex; i < (runStartIndex + runLength); i++){

        prob = prob + probdif

        newPrice1 = (1.0 / prob).toFixed(2)

        newPrice2 = getPriceFromTicks(getTicksFromPrice(newPrice1) - 2).toFixed(2)

       

        let record ={

                        "layprice1": newPrice1,

                        "backprice1": newPrice2,

                        "wom": wom.toFixed(2)

                       

        }

        sequence.push(record)



    }

    for(let i= (runStartIndex + runLength); i< (inputSequenceLength + outputSequenceLength); i++){

        let record ={

                        "layprice1": newPrice1,

                        "backprice1": newPrice2,

                        "wom":0.0

                       

        }

        sequence.push(record)

    }



    //console.log(sequence)

    sequence.map((record) => {

        console.log(runningCount++ + "," + record.layprice1 + "," + record.backprice1 + "," + record.wom)

    })

 

}

 

for(let i=0;i< 10000;i++){

    generateSequence(10,5, 5)

}

 

 

//console.log(getPriceFromTicks(101))

 

 

 

 

