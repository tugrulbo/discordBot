import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
from discord.utils import get
import datetime
import youtube_dl
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import youtube_dl as yt
from youtube_search import YoutubeSearch


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
        
#Eğer discord için bot yazıyorsanız ve class kullandıysanız komutlarda self kullanmalısınız
class CommandsEvents(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
   
    @commands.command(name='play')
    async def play(self,ctx):
      if ctx.message.content.startswith('.play Youtube'):
          channel = ctx.message.author.voice.channel
          voice = get(self.bot.voice_clients, guild=ctx.guild)

          if voice and voice.is_connected():
             await voice.move_to(channel)
          else:
             voice = await channel.connect()

          await voice.disconnect()

          if voice and voice.is_connected():
             await voice.move_to(channel)
          else:
             voice = await channel.connect()
             print(f"Bağlanılan Kanal: {channel}\n")

          await ctx.send(f"{channel} Girildi")

          new_url = ctx.message.content
          _replaceUrl = new_url.replace(".play Youtube","")
          async with ctx.typing():
              player = await YTDLSource.from_url(_replaceUrl, loop=self.bot.loop, stream=True)
              ctx.voice_client.play(player, after=lambda e: print('Oynatıcı Hatası: %s' % e) if e else None)
          await ctx.send('Şuan oynatılıyor: {}'.format(player.title))
    
      if ctx.message.content.startswith('.play Spotify'):
         scope = "user-library-read"
         _splitMessage = ctx.message.content
         _splitLink = _splitMessage.replace('.play Spotify',"")
         print(_splitLink) 
         song = _splitLink

         sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='CLIENT ID',client_secret='CLIENT SECRET'))
         results = sp.track(song)
         print(results['name'])
         _song = results['name']
         _uri = results['uri']
         _songArtist = sp.track(_uri)
         _Artist = _songArtist['artists']
         _jsonPart = json.dumps(_Artist)
         _findArtist = sp.artist(_jsonPart[32:86])
         print(_findArtist['name'])
         _youtubeArtist = _findArtist['name']
         results1 = YoutubeSearch(f'{_song} {_youtubeArtist}', max_results=1).to_json()
         _youtubeSearch= results1.split(':')
         _myLinkLast = _youtubeSearch[len(_youtubeSearch)-1].replace('"}]}','')
         _myLinkStart = _myLinkLast.replace('"/','')
         print(_myLinkStart) 
         _myYoutubeURL = _myLinkStart.strip()
         channel = ctx.message.author.voice.channel
         voice = get(self.bot.voice_clients, guild=ctx.guild)

         if voice and voice.is_connected():
             await voice.move_to(channel)
         else:
             voice = await channel.connect()

         await voice.disconnect()

         if voice and voice.is_connected():
             await voice.move_to(channel)
         else:
             voice = await channel.connect()
             print(f"Bağlanılan Kanal: {channel}\n")

         await ctx.send(f"{channel} Girildi")

         new_url = ctx.message.content
         _replaceUrl = f"https://www.youtube.com/{_myYoutubeURL}"
         print(_replaceUrl)
         async with ctx.typing():
              player = await YTDLSource.from_url(_replaceUrl, loop=self.bot.loop, stream=True)
              ctx.voice_client.play(player, after=lambda e: print('Oynatıcı Hatası: %s' % e) if e else None)
         await ctx.send('Şuan oynatılıyor: {}'.format(player.title))
   
    @commands.command(name='volume')
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send(
                
                "Herhangi bir ses kanalına bağlı değil")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Ses seviyesi: {}%".format(volume))
    

    @commands.command(name='leave')
    async def leave(self,ctx):
       channel = ctx.message.author.voice.channel
       voice = get(self.bot.voice_clients, guild=ctx.guild)

       if voice and voice.is_connected():
          await voice.disconnect()
          print(f"Bot ayrıldı: {channel}")
          await ctx.send(f"{channel} ayrıldı")
       else:
          print("Bot was told to leave voice channel, but was not in one")
          await ctx.send("Herhangi bir ses kanalında olduğunu düşünmüyorum.")
       
    
    
def setup(bot):
    bot.add_cog(CommandsEvents(bot))