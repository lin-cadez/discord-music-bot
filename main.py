import discord
from discord.ext import commands,tasks
import os
import time
import requests
import csv
import youtube_dl
from youtubesearchpython import *
from pytube import YouTube

skip_music=[]


intents = discord.Intents().all()
#client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='!',intents=intents)



class bot():
    """docstring for bot"""

    async def play(self, message):
        user=str(message.author).split("#")[0]
        server = message.guild
        channel = message.author.voice.channel
        voice_channel = server.voice_client
        message_input=message.content.replace(".play ", "").lower()
        try: 
            await channel.connect()
        except:
            pass
        try:
            await voice_channel.stop()
        except:
            pass


        url, title=self.get_url(message_input)
        print(url, "check")



        if url == False:
            await message.channel.send("Error 404")
        else:

            print(url, title)

            print(self.is_url(url))
            if self.is_url(url):

                #skip_music.append(url)


                #začne s postopkom pridobivanja file in predvajanja
                print("Song: ", title)
                await message.channel.send("Song: " + title)
                file_name=self.get_file(url, title)
                
                print(file_name, "je to")
                if file_name:
                    



                    #try:
                    print("to je filename:  ", file_name)
                    channel = message.author.voice.channel
                    voice_channel = server.voice_client
                    voice_client=server.voice_client
                    file_name=os.path.basename(file_name)


                    
                    voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=file_name))
                    print("Playing")

                        
                        
                    #except:
                    #print("funkcija play, Napaka s predvajanje, poskusi ponovno!!!")




                    
                else:
                    print("try another song")
                    await message.channel.send("Song may disrespect guidlines or it is a live stream")

            else:
                print("Napaka pri odpiranju url-ja")

    async def leave(self, message):
        try:
            server = message.guild
            channel = message.author.voice.channel
            voice_channel = server.voice_client
            voice_client=server.voice_client
            await voice_client.disconnect()
        except:
            await message.channel.send("Bot is not joined in any of voice channels. Use command .join to activate the bot.")
            time.sleep(0.3)
            print("Napaka v Leave funkciji")


    async def join(self, message):
        try:
            user=str(message.author).split("#")[0]
            server = message.guild
            channel = message.author.voice.channel
            voice_channel = server.voice_client
            await channel.connect()
        except:
            await message.channel.send(f"{user} You need to join voice channel first.")
            print("Napaka v funkciji join")

    async def stop(self, message):
        try:
            user=str(message.author).split("#")[0]
            server = message.guild
            channel = message.author.voice.channel
            voice_channel = server.voice_client
            await voice_channel.stop()
        except:
            #await message.channel.send(f"{user} Neki problem s stopom")
            print("Error in stop function")
        

    def is_url(self, url):
        if "https://www.youtube.com/" in url or "https://youtu.be/" in url:

            url="https://www.youtube.com/oembed?url="+url
            r = requests.get(url)
            if "200" in str(r):
                return True
            else:
                return False

    def get_url(self, song):
        customSearch = VideosSearch(song, limit = 1)
        result=customSearch.result()

        if len(result["result"])==0:
            print("ni rezultatov isikanja")

            return False, False

        elif len(result["result"])==1:
            title=result["result"][0]["title"]
            video_id=result["result"][0]["id"]
            url=f"https://www.youtube.com/watch?v=" + video_id
            return url, title

        else:
            print("rezultatov je več kot 1? baje")

            return False, False


    def get_file(self, url, title):
        file_to_search=title+".mp3"
        file_search=os.path.exists(file_to_search)
        

        if file_search:
            return file_to_search

        else:

            try:
                yt = YouTube(url)
                video = yt.streams.filter(only_audio=True).first()
                path=os.path.abspath(os.getcwd())
                #os.path.exists()
                out_file = video.download(output_path=path)
                base, ext = os.path.splitext(out_file)
                filename = base + '.mp3'
                filename4 = base + '.mp4'
                print(filename)
                try:
                    os.rename(out_file, filename)
                
                except:
                    os.remove(filename4)
                    
                    
                return filename
            except:
                return False

        
bot=bot()



#definiranje komand
@client.event
async def on_message(message):

    server = message.guild           
    user=str(message.author).split("#")[0]
    

    start_time = time.time()

    if not message.author.bot:



        if ".join" in message.content:
            await bot.join(message)
            

        if ".stop" in message.content:
            await bot.stop(message)


        if ".out" in message.content or ".leave" in message.content:
            await bot.leave(message)
                

        if ".play " in message.content:
            await bot.play(message)
            await client.change_presence(activity=discord.Game(name="with fire."))


            print("--- %s seconds ---" % (time.time() - start_time))






if __name__ == "__main__" :
    client.run("token")
