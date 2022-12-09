# load packages
library(ggplot2)
library(lubridate)
library(ggthemes)
library(rjson)
library(scales)

# create fake data DF
df_historical <- data.frame(
    date = c(today() -6, today() -5, today() -4, today() -3, today() -2, today() -1, today()),
    stock_price = c(2.3, 3.4, 5.2, 3.2, 4.5, 3.2, 2.1)
  )

df_prediction <- data.frame(
    date = c(today() +1, today() +2, today() +3, today() +4, today() +5, today() +6, today() + 7, 
             today() +8, today() +9, today() +10, today() +11, today() +12, today() +13, today() + 14),
    stock_price = c(2.3, 3.4, 1.2, 2.2, 4.3, 3.2, 4.1, 2.3, 3.4, 1.2, 2.2, 4.3, 3.2, 4.1)
  )

# merge DFs
df = rbind(df_historical, df_prediction)
  

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
  geom_point(aes(colour = date < today()), size = 5) +
  
  # vertical line for today
  geom_vline(data = df, mapping = aes(xintercept = date[7]), linetype = 'dashed',
               color = 'darkgreen', size = 1) +
  geom_label(aes(x=date[7], y= max(stock_price)), label= 'Today', fill = 'white') +
  
  # labels and axes
  labs(title = 'Price in the past and our prediction',
         subtitle = 'stock_name') +
  xlab('') +
  ylab('P r i c e\n') +
  
  # theme
  theme_economist() +
  scale_colour_manual(name = '', values = c('deeppink4','darkgrey')) +
  
  theme(axis.text.x = element_text(face = 'bold',
                                   angle = 75, vjust = 0.5, 
                                   color = price_color), 
        text = element_text(size = 13), 
        legend.position = 'none') +
  scale_x_continuous(breaks = pretty(df$date, n = 21)) # to return all tickers on the x axis

stock_plot

ggsave('~/code/rahulvaity25/stock_prediction/stock_prediction/r_docker/stock_plot.png', stock_plot, device = 'png')

