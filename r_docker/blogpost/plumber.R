# load packages
library(ggplot2)
library(lubridate)
library(ggthemes)
library(rjson)
library(plumber)
library(scales)

##### ENDPOINT 1 - PLOT
#* @param stock_prediction 
#* @post /plot
# @get /plot
#* @serializer png
function(stock_prediction){
  # get name of stock
  stock_name = stock_prediction$stock
  
  # create REAL DF
  df_historical <- data.frame(
    # date = stock_prediction$stock_date,
    date = tail(stock_prediction$stock_date, 7),
    stock_price = tail(stock_prediction$stock_price, 7)
  )
  
  df_historical$date = as.Date(as.POSIXct(df_historical$date/1000000000, origin="1970-01-01")) # convert nanoseconds to date
  df_historical <- subset(df_historical, date > as.Date("2022-09-01"))  # ignore missing values which are treated as "1970-01-01"
  
  df_prediction <- data.frame(
    date = c(today() +1, today() +2, today() +3, today() +4, today() +5, today() +6, today() + 7,
             today() +8, today() +9, today() +10, today() +11, today() +12, today() +13, today() + 14),
    stock_price = stock_prediction$stock_prediction_14
  )
  
  # merge DFs
  df = rbind(df_historical, df_prediction)
  
  # get dates correctly
  start_date = as.Date(today() - 6)
  last_date = as.Date(today() + 14)
  dates = seq(from = start_date, to = last_date, by = 'day')
  
  df$date <-  dates
  
  ##### PLOT

  # set condition for date color
  price_color <- ifelse(df$stock_price == max(df$stock_price), "red",   # mark highest price
                        ifelse(df$stock_price == min(df$stock_price), "blue",   # mark lowest price
                               "black"))
  # build plot
  stock_plot = ggplot(df,
                      mapping = aes(x=date, y=stock_price)) +

    # plot lines
    geom_line() +
    geom_point(aes(colour = date < (today() + 1)), size = 5) +

    # vertical line for today
    geom_vline(data = df, mapping = aes(xintercept = date[7]), linetype = 'dashed',
               color = 'darkgreen', size = 1) +
    geom_label(aes(x=date[7], y= max(stock_price)), label= 'Today', fill = 'white') +

    # labels and axes
    labs(title = 'Price in the past and our prediction',
         subtitle = stock_name) +
    xlab('') +
    ylab('P r i c e\n') +

    # theme
    theme_economist() +
    scale_colour_manual(name = '', values = c('deeppink4','darkgrey')) +

    theme(axis.text.x = element_text(face = 'bold',
                                     angle = 90, vjust = 0.5,
                                     color = price_color),
          text = element_text(size = 13),
          legend.position = 'none') +
    scale_x_continuous(breaks = pretty(df$date, n = 21)) # to return all tickers on the x axis


  print(stock_prediction)
  print(stock_plot)
  
}


