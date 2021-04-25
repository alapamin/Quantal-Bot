import discord
from discord.ext import commands,tasks
import os
import yfinance as yf
import asyncio
from datetime import date, datetime, timedelta
from threading import Timer
import requests
import numpy as np
from keep_live import keep_alive

''' 
        necessary params to access
        discord bot api and other api's

'''


token = os.getenv('token')
rKey = os.getenv('rKey')
rHost = os.getenv('rHost')



''' 

        class for discord client
        found this way easier than using bot or regular
        client commands (might change later for optimal bot performance)

'''

class MyClient(discord.Client):
    async def on_ready(self):
        await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name = "the Stock Market"))
        print('Logged in as', client.user.name)

    
    ''' 

        a single async function for all commands
        still figuring out discord api :(

    '''


    async def on_message(self, message: discord.message.Message):

        if message.author.id != client.user.id:

          ''' 

              first command $stock takes in a ticker
              then uses yfinance api to return dailyhigh,
              dailylow, current price and previous close

              other returns are for the discord embed method

              try except is to catch errors, an error would be
              an invalid ticker, instead of returning error to console it
              catches error and returns a message for the user to try again

          '''

          try:

            if message.content.startswith('$stock'):
              await message.channel.trigger_typing()
              stock = message.content.split(' ')[1].upper()
              ticker = yf.Ticker(stock)


              s_current = ticker.info.get('regularMarketPrice')
              s_high = ticker.info.get("dayHigh")
              s_low = ticker.info.get("dayLow")
              s_url = ticker.info.get("website")
              s_name = ticker.info.get("longName")
              s_logo = ticker.info.get("logo_url")
              prev_close = ticker.info.get("previousClose")
              prev_open = ticker.info.get("regularMarketOpen")

              embed=discord.Embed(
              title= stock,
                  url=s_url,
                  description=f"Stock info for {s_name}" ,
                  color=discord.Color.purple())
              embed.set_author(name=f"{s_name}", url=f"{s_url}", icon_url=f"{s_logo}")
              embed.add_field(name = "**Current Price**", value=f"${s_current}", inline = False)    
              embed.add_field(name="**Day High**", value=f"${s_high}", inline=False)
              embed.add_field(name="**Day Low**", value=f"${s_low}", inline=False)
              embed.add_field(name = "**Previous Open**", value = f"${prev_open}", inline = False)
              embed.add_field(name = "**Previous Close**", value = f"${prev_close}", inline = False)


              await message.channel.send(embed = embed)

          except (ImportError, KeyError):

            embedError=discord.Embed(color=discord.Color.purple())
            embedError.add_field(name="Error", value="Invalid Ticker, try again")
            await message.channel.send(embed = embedError)
          
          ''' 

              second command $split takes in ticker
              and returns all splits for the ticker

          '''

          try:
              
            if message.content.startswith('$split'):
              await message.channel.trigger_typing()
              stock = message.content.split(' ')[1].upper()
              ticker = yf.Ticker(stock)
              s_url = ticker.info.get("website")
              s_name = ticker.info.get("longName")
              s_logo = ticker.info.get("logo_url")
              splits = ticker.splits
              embed = discord.Embed(
              title = stock,
                url = s_url,
                description = f"Splits for {s_name}",
                color = discord.Color.purple())
              embed.set_author(name = f"{s_name}", url = f"{s_url}", icon_url = f"{s_logo}")
              embed.add_field(name = "**Splits**", value = f"{splits}")

              await message.channel.send(embed = embed)

          except (ImportError, KeyError):

            embedError=discord.Embed(color=discord.Color.purple())
            embedError.add_field(name="Error", value="Invalid Ticker, try again")
            await message.channel.send(embed = embedError)


          

          ''' 

              third command dividends will take in
              a ticker then return the dividends for
              the ticker

              currently the first api does not work well
              with retreiving calls from yahoo finance for
              stock dividends, command still in working progress

          '''

          # if message.content.startswith('$div'):
          #   stock = message.content.split(' ')[1].upper()
          #   ticker = yf.Ticker(stock)
          #   s_url = ticker.info.get("website")
          #   s_name = ticker.info.get("longName")
          #   s_logo = ticker.info.get("logo_url")
          #   div = ticker.dividends
          #   print("div started")
          #   embed = discord.Embed(
          #   title = stock,
          #     url = s_url,
          #     description = f"Dividends for {s_name}",
          #     color = discord.Color.purple())
          #   embed.set_author(name = f"{s_name}", url = f"{s_url}", icon_url = f"{s_logo}")
          #   embed.add_field(name = "**Dividends**", value = f"{div}")


          ''' 

              fourth command $trend returns the current
              trending stocks according to yfinance

              later it will also automatically send
              trending tickers to server 3 times a day

          '''

          try:

            if message.content.startswith('$trend'):
              await message.channel.trigger_typing()
              url="https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-trending-tickers"

              querystring = {"region":"US"}   
              
              headers = {
                'x-rapidapi-key': rKey,
                'x-rapidapi-host': rHost
        }
              
              response = requests.request("GET", url, headers=headers, params=querystring)

              r2 = response.json()

              # stonk 1
              
              q1 = r2["finance"]['result'][0]['quotes'][0]
              stonk1 = q1['symbol']
              stock1_market_price = q1['regularMarketPrice']
              s1MCP = q1['regularMarketChangePercent']
              stock1_market_change_per = (float(np.round(s1MCP, 2)))
            


              # stonk 2
              q2 = r2["finance"]['result'][0]['quotes'][1]
              stonk2 = q2['symbol']
              stock2_market_price = q2['regularMarketPrice']
              s2MCP = q2['regularMarketChangePercent']
              stock2_market_change_per = (float(np.round(s2MCP, 2)))
              


              # stonk 3
              q3 = r2["finance"]['result'][0]['quotes'][2]
              stonk3 = q3['symbol']
              stock3_market_price = q3['regularMarketPrice']
              s3MCP = q3['regularMarketChangePercent']
              stock3_market_change_per = (float(np.round(s3MCP, 2)))
              

              # stonk 4
              q4 = r2["finance"]['result'][0]['quotes'][3]
              stonk4 = q4['symbol']
              stock4_market_price = q4['regularMarketPrice']
              s4MCP = q4['regularMarketChangePercent']
              stock4_market_change_per = (float(np.round(s4MCP, 2)))
              


              # stonk 5
              q5 = r2["finance"]['result'][0]['quotes'][4]
              stonk5 = q5['symbol']
              stock5_market_price = q5['regularMarketPrice']
              s5MCP = q5['regularMarketChangePercent']
              stock5_market_change_per = (float(np.round(s5MCP, 2)))
              
              

              embed = discord.Embed(
              title = "Trending Tickers",
              description = "This is a list of the current top 5 trending tickers in the stock market. (Information from Yahoo Finance)" ,
                color = discord.Color.purple())


              embed.add_field(name = "Stock", value=f"{stonk1} \n {stonk2} \n {stonk3} \n {stonk4} \n {stonk5}", inline = True)

              embed.add_field(name = "Price", value = f"${stock1_market_price} \n ${stock2_market_price} \n ${stock3_market_price} \n ${stock4_market_price} \n ${stock5_market_price}", inline = True)

              embed.add_field(name = "Change", value = f"{stock1_market_change_per}% \n {stock2_market_change_per}% \n {stock3_market_change_per}% \n {stock4_market_change_per}% \n {stock5_market_change_per}%", inline = True)

              await message.channel.send(embed = embed)

          except (ImportError, KeyError):

            embedError=discord.Embed(color=discord.Color.purple())
            embedError.add_field(name="Error", value="Invalid Ticker, try again")
            
            await message.channel.send(embed = embedError)


          
            ''' 
            
                fifth command will accept inputs
                from the command list then return
                the available commands and what they do

                this command is still in the works currently
                i have to hard code every command and it's functionality
                to be returned to the user

            '''

          #.startswith is not a discord function its a python built in funciton

          command_list = ['$help', '$commands'] #this list

          if message.content.startswith(tuple(command_list)):
            await message.channel.trigger_typing()
            embed = discord.Embed(
              title="Quantal Bot Help",
              description="Command List: ",
              colour = discord.Colour.purple())
            embed.add_field(name="$stock (ticker)",value="Gives the day's high and low value for a stock",inline=False)

            embed.add_field(name="$split (ticker)",value='Gives the quantity of splits a stock has had, which lowers the price of a share to allow for an increase in quantity of investors',inline=False)

            embed.add_field(name="$div (ticker)",value='Shows the dividends for the ticker (WIP)',inline=False)

            embed.add_field(name="$trend",value='Shows the current trending stocks according to Yahoo Finance (WIP)',inline=False)

            embed.add_field(name="$chart (ticker)",value='Shows the current chart for a ticker',inline=False)

            embed.add_field(name="$help",value='Shows commands and their descriptions. ',inline=False)
            embed.set_footer(text="Created by Quantal & Co. ©")
            await message.channel.send(embed=embed)
          


          ''' 
          
              my favorite command and the command that took the most out of me
              sixth command $chart takes in a ticker and returns the current
              chart for the ticker
              
              no api worked well with charts so i decided to pull some tricks
              out my sleeve

              works well for now

          '''
          

          try:

            if message.content.startswith('$chart'):
              await message.channel.trigger_typing()
              stock = message.content.split(' ')[1].upper()
              ticker = yf.Ticker(stock)
              s_url = ticker.info.get("website")
              s_name = ticker.info.get("longName")
              s_logo = ticker.info.get("logo_url")
              s_high = ticker.info.get("dayHigh")
              
              # chart =  'https://www.tradingview.com/chart/?symbol=NYSE%3A' + stock
              
              # chart = 'https://www.barchart.com/stocks/quotes/'+ stock + '/interactive-chart'

              chart =  'https://stockcharts.com/c-sc/sc?s=' + stock + '&p=D&b=5&g=0&i=0&r=1615008274751'
            
              embed=discord.Embed(
                color=discord.Color.purple())
              embed.set_author(name=f"{s_name}", url=f"{s_url}", icon_url=f"{s_logo}")     
              embed.set_image(url = chart)
              await message.channel.send(embed = embed)
          except (ImportError, KeyError):

            embedError=discord.Embed(color=discord.Color.purple())
            embedError.add_field(name="Error", value="Invalid Ticker, try again")
            
            await message.channel.send(embed = embedError)
          

          ''' Restart command in the works
        
          
          if message.content.startswith('$restart'):
            if message.author.has_role('Quantal' or 'Quantal Team'):
              await message.channel.trigger_typing()
              restart = await message.channel.send("Restarting...")

              await restart.delete()
              
              await asyncio.sleep(3)
              
              await message.client.logout()
              
              await message.client.login()
          '''








          ''' 
          
          demo command not sure if it'll work
          
          '''
          
          try:


            x = datetime.today()
            y = x.replace(day = x.day+1, hour = 11, minute = 0, second = 0, microsecond = 0) + timedelta(days = 1)
            delta_t = y-x
            secs = delta_t.total_seconds()

            async def trendTimer():

              await message.channel.trigger_typing()
              url="https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-trending-tickers"

              querystring = {"region":"US"}   
                
              headers = {
                'x-rapidapi-key': rKey,
                'x-rapidapi-host': rHost
          }
                
              response = requests.request("GET", url, headers=headers, params=querystring)

              r2 = response.json()

              # stonk 1
                
              q1 = r2["finance"]['result'][0]['quotes'][0]
              stonk1 = q1['symbol']
              stock1_market_price = q1['regularMarketPrice']
              s1MCP = q1['regularMarketChangePercent']
              stock1_market_change_per = (float(np.round(s1MCP, 2)))
            


              # stonk 2
              q2 = r2["finance"]['result'][0]['quotes'][1]
              stonk2 = q2['symbol']
              stock2_market_price = q2['regularMarketPrice']
              s2MCP = q2['regularMarketChangePercent']
              stock2_market_change_per = (float(np.round(s2MCP, 2)))
              


              # stonk 3
              q3 = r2["finance"]['result'][0]['quotes'][2]
              stonk3 = q3['symbol']
              stock3_market_price = q3['regularMarketPrice']
              s3MCP = q3['regularMarketChangePercent']
              stock3_market_change_per = (float(np.round(s3MCP, 2)))
              

              # stonk 4
              q4 = r2["finance"]['result'][0]['quotes'][3]
              stonk4 = q4['symbol']
              stock4_market_price = q4['regularMarketPrice']
              s4MCP = q4['regularMarketChangePercent']
              stock4_market_change_per = (float(np.round(s4MCP, 2)))
              


              # stonk 5
              q5 = r2["finance"]['result'][0]['quotes'][4]
              stonk5 = q5['symbol']
              stock5_market_price = q5['regularMarketPrice']
              s5MCP = q5['regularMarketChangePercent']
              stock5_market_change_per = (float(np.round(s5MCP, 2)))
              
              

              embed = discord.Embed(
              title = "Trending Tickers",
              description = "This is a list of the current top 5 trending tickers in the stock market. (Information from Yahoo Finance)" ,
                color = discord.Color.purple())


              embed.add_field(name = "Stock", value=f"{stonk1} \n {stonk2} \n {stonk3} \n {stonk4} \n {stonk5}", inline = True)

              embed.add_field(name = "Price", value = f"${stock1_market_price} \n ${stock2_market_price} \n ${stock3_market_price} \n ${stock4_market_price} \n ${stock5_market_price}", inline = True)

              embed.add_field(name = "Change", value = f"{stock1_market_change_per}% \n {stock2_market_change_per}% \n {stock3_market_change_per}% \n {stock4_market_change_per}% \n {stock5_market_change_per}%", inline = True)

              await message.channel.send(embed = embed)
            t = Timer(secs, trendTimer)
            t.start()

          except (ImportError, KeyError):

            embedError=discord.Embed(color=discord.Color.purple())
            embedError.add_field(name="Error", value="Invalid Ticker, try again")
            
            await message.channel.send(embed = embedError)




keep_alive()
client = MyClient()
client.run(token)

