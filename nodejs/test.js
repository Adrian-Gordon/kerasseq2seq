const chai = require('chai')
const {expect} = chai
const Trader  = require('./trader.js').Trader

describe('Unit tests: Trader', () => {
  it('should return the correct number of ticks for prices less than 2.0', () => {
    expect(Trader.getTicks(1.64)).to.equal(64)
  })
  it('should return correct number of ticks', () => {
    expect(Trader.getTicks(6.6)).to.equal(193)
  })
  it('should correctly increment a price below 2.0', () => {
    expect(Trader.incrementPrice(1.5, 10)).to.equal(1.6)
  })
  it('should correctly increment a price', () => {
    expect(Trader.incrementPrice(1.64, 129)).to.equal(6.6)
  })
  it('should return true if it is trading opportunity', () => {
    expect(Trader.isTradingOpportunity(6.6, 1.64, 60)).to.be.true
  })
  it('should return false if not enough ticks', () => {
    expect(Trader.isTradingOpportunity(6.6, 1.64, 200)).to.be.false
  })
  it('should return false if negative ticks', () => {
    expect(Trader.isTradingOpportunity(1.64, 6.6, 60)).to.be.false
  })
  it('should be a winning back to lay trade', () => {
    const res = Trader.simulateBackToLayTrade(6.6, 10, 3.4)
    expect(res.returns > 0).to.be.true
  })
  it('should be a losing back to lay trade', () => {
    const res = Trader.simulateBackToLayTrade(3.4, 10, 6.6)
    expect(res.returns > 0).to.be.false
  })
  it('should be a winning lay to back trade', () => {
    const res = Trader.simulateLayToBackTrade(3.4, 10, 6.6)
    expect(res.returns > 0).to.be.true
  })
  it('should be a losing lay to back trade', () => {
    const res = Trader.simulateLayToBackTrade(6.6, 10, 3.4)
    expect(res.returns > 0).to.be.false
  })
  it('should take a profit from a back to lay trade', () => {
    const res = Trader.simulateBackToLay(3.0, 10.0, [3.0, 2.9, 2.8, 2.7, 2.6, 2.5], 10, -10)
    expect(res.returns > 0).to.be.true
  })
  it('should stop loss for a back to lay trade', () => {
    const res = Trader.simulateBackToLay( 3.0, 10.0, [3.0, 3.1, 3.2, 3.3, 3.4, 3.5], 10, -10)
    expect(res.returns < 0.0).to.be.true
  })
  it('should close position for a back to ly trade', () => {
    const res = Trader.simulateBackToLay( 3.0, 10.0, [3.0, 3.1, 3.0, 3.1, 3.0, 3.1, 3.0], 10, -10)
    expect(res.returns == 0.0).to.be.true
  })
  it('should take a profit from a lay to back trade', () => {
    const res = Trader.simulateLayToBack(3.0, 10.0, [3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.4, 3.4], 10, -10)
    expect(res.returns > 0.0).to.be.true
  })
  it('should stop loss for a lay to back trade', () => {
    const res = Trader.simulateLayToBack(3.0, 10.0, [3.0, 2.9, 2.8, 2.7, 2.6, 2.5], 10, -10)
    expect(res.returns < 0.0).to.be.true
  })
  it('should close position for a lay to back trade', () => {
    const res = Trader.simulateLayToBack(3.0, 10.0, [3.0, 3.1, 3.2, 3.3, 3.3, 3.3, 3.3, 3.3, 3.0], 10, -10)
    expect(res.returns == 0.0).to.be.true
  })
})