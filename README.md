## INTRO
This is automated trading bot.
                                                                                      
## HOWTO
```...```

## CODE STRUCTURE
```data manager```
* historical data
* live data

```indicators manager```
* various indicators used for strategies

```strategy manager aka trader```
* implements certain strategy and handle orders

```orders manager```
* handles orders

## TODO
- [ ] to implement "stop loss watchod"
      read data every 15 minutes and execute bot on 4H hour only [00:00, 04:00, ..., 20:00] 
      but stop losses to be monitored every 5 min;
- [ ] to backtest various pct_change stop losses and select optimum value based on hist data;
- [ ] to add live trading;
- [ ] to implement multiple orders per Trader;
- [ ] to use various data sources e.g. network hashrate, OI, Volume

## CONTRIBUTION
```...```                                                                                            
