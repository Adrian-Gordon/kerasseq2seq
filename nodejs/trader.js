ticksLookup=[
  [2.0, 100, 100, 0.02],
  [3.0, 50, 150, 0.05],
  [4.0, 20, 170, 0.1],
  [6.0, 20, 190, 0.2],
  [10.0, 20, 210, 0.5],
  [20.0, 20, 230, 1.0],
  [30.0,10, 240, 2.0],
  [50.0, 10, 250, 5.0]
  ]

class Trader{
  constructor(){

  }

  static getTicks(price){
    let ticks = 0
    let index = -1
    for(let i=0; i<ticksLookup.length; i++ ){
      if(price > ticksLookup[i][0])
        index+=1
      else  if(index > -1){
        ticks = ticksLookup[index][2]
        const dif = price - ticksLookup[index][0]
        const dif_in_ticks = dif /(ticksLookup[index][3])
        ticks += dif_in_ticks
      }

    }
    if(index == -1){
      ticks = (price - 1.0) / 0.01
    }

    return Math.round(ticks)
  }

  static incrementPrice(price, ticks){
    const priceTicks = Trader.getTicks(price)
    const targetTicks = priceTicks + ticks
    let index = -1
    for(let i = 0; i< ticksLookup.length; i++){
      if(ticksLookup[i][2] > targetTicks){
        index = (i - 1)
        break
      }
    }
    if(index == -1){
        return(price + (ticks * 0.01))
    }

    const remainingTicks = targetTicks - ticksLookup[index][2]
    const priceIncrement = remainingTicks * ticksLookup[index][3]
    const targetPrice = ticksLookup[index][0] + priceIncrement
    return(targetPrice)
  }

  static isTradingOpportunity(backPrice, layPrice, ticks){
    const backTicks = Trader.getTicks(backPrice)
    const layTicks = Trader.getTicks(layPrice)
    if((backTicks - layTicks) > ticks){
      return(true)
    }
    else{
      return(false)
    }
  }

/*
        Simulate the operation of a back to lay trade against a time series of observed lay prices
        parameters:
          oddsToBack -- float, odds at which to place the starting back bet
          stakeToBack -- float, stake at which to place the starting back bet
          lObserved -- array of floats, observed sequence of lay prices
          targetTicks -- integer, target number of ticks difference before trading out for a profit
          stopLossTicks -- negative integer, maximum number of ticks of loss to accept before performing a stop loss process
        returns:
          float: return on the trade
  */
  static simulateBackToLay(oddsToBack, stakeToBack, lObserved, targetTicks, stopLossTicks){
      const backedTicks = Trader.getTicks(oddsToBack)
      let observedPrice
      for(let t = 0; t <  lObserved.length; t++){
        observedPrice = lObserved[t]
        const observedTicks = Trader.getTicks(observedPrice)

        const tickDiff = backedTicks - observedTicks 


        if(tickDiff >= targetTicks){
          return Trader.simulateBackToLayTrade(oddsToBack, stakeToBack, observedPrice) //take profit
          break
        }
        if(tickDiff <= stopLossTicks){
          return Trader.simulateBackToLayTrade(oddsToBack, stakeToBack, observedPrice) //stop loss
          break
        }
      }

      return Trader.simulateBackToLayTrade(oddsToBack, stakeToBack, observedPrice) //close position
  }

  static simulateLayToBack(oddsToLay, stakeToLay, bObserved, targetTicks, stopLossTicks){
    /*
      Simulate the operation of a lay to back trade against a times eries of observed back prices
      parameters:
        oddsToLay -- float, odds at which to place the starting lay bet
        stakeToLay -- float, stake at which to place the starting lay bet i.e. amount to lose
        bObserved -- array of floats, observed sequence of back prices
        targetTicks -- integer, target number of ticks difference before trading out for a profit
        stopLossTicks -- negative integer, maximum number of ticks of loss to accept before performing a stop loss process
      returns:
        float: return on the trade
    */
    

    const layedTicks = Trader.getTicks(oddsToLay)
    let observedPrice
    for(let t  = 0; t < bObserved.length; t++){
       observedPrice = bObserved[t]
      const observedTicks = Trader.getTicks(observedPrice)

      const tickDiff = observedTicks - layedTicks


      if(tickDiff >= targetTicks){
        return Trader.simulateLayToBackTrade(oddsToLay, stakeToLay, observedPrice) //take profit
        break
      }
      if(tickDiff <= stopLossTicks){
        return Trader.simulateLayToBackTrade(oddsToLay, stakeToLay, observedPrice) //stop loss
        break
      }
    }
    return Trader.simulateLayToBackTrade(oddsToLay, stakeToLay, observedPrice) //close position

  }



  static simulateBackToLayTrade(backOdds, backStake, layOdds){
    /*simulate the placing of a back to lay trade
      parameters:
        backOdds -- float, the decimal odds of the back half of the trade
        backStake -- float, the stake on the back side of the trade
        layOdds -- float, the decimal odds of the lay part of the trade
      returns:
        float, the return on the trade
      */

    const layStake = backStake / ((layOdds /(layOdds -1.0)) / backOdds)

    const returnVal = {
      'returns':(backStake * (backOdds -1)) - layStake, 
      'backOdds':backOdds,
      'backStake': backStake, 
      'layOdds':layOdds, 
      'layStake': layStake
    }

    return(returnVal)
  }

  static simulateLayToBackTrade(layOdds, layStake, backOdds){
    /*simulate the placing of a lay to back trade
    parameters:
      layOdds -- float, the decimal odds of the lay part of the trade
      layStake -- float, the stake on the lay side of the trade (amount layed to lose)
      backOdds -- float, the decimal odds of the back half of the trade
    returns:
      float, the return on the trade
      */
      const backStake = layStake * ((layOdds /(layOdds -1.0)) / backOdds)

      const returnVal = {
        'returns': (backStake * (backOdds -1)) - layStake,
        'backOdds':backOdds,
        'backStake': backStake, 
        'layOdds':layOdds, 
        'layStake': layStake
      }

      return(returnVal)


  }
}

module.exports = { Trader }