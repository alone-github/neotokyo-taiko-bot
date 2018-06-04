import discord
import valve.source.a2s
import valve.source.master_server

client = discord.Client()

@client.event
async def on_message(message):
# outputs status of all nt servers
    if message.content.startswith('!all'):

# queries something master server 
# creates dict status, where key is "server ip:port"
        status = {}
        with valve.source.master_server.MasterServerQuerier() as msq:
            try:
                for address in msq.find(gamedir="NeotokyoSource"):
                    with valve.source.a2s.ServerQuerier(address) as server:
                        info = server.info()
                        players = server.players()
                        status[str(address[0]) + str(":") + str(address[1])] = dict(info)
            except valve.source.NoResponseError:
                pass

        embed = discord.Embed(description="```css\nAll Servers```", 
                      color=0xF6B26B)
    
        for ii in status.keys():
            embed.add_field(name=status[ii]['server_name'], 
                            value=str(status[ii]['player_count']) + "/" + str(status[ii]['max_players']) + " :: " + str(status[ii]['map']), 
                            inline=False)
        await client.send_message(message.channel, embed=embed)
# outputs on active servers, i.e. with players    
    if message.content.startswith('!active'):
        
        status = {}
        
        with valve.source.master_server.MasterServerQuerier() as msq:
            try:
                for address in msq.find(gamedir="NeotokyoSource"):
                    with valve.source.a2s.ServerQuerier(address) as server:
                        info = server.info()
                        players = server.players()
                        status[str(address[0]) + str(":") + str(address[1])] = dict(info)
            except valve.source.NoResponseError:
                pass

        embed = discord.Embed(description="```css\nActive Servers```", 
                              color=0x00FF00)
        if {k:v for k,v in status.items() if v['player_count'] > 0} != {}:
            for ii in {k:v for k,v in status.items() if v['player_count'] > 0}.keys():
                    embed.add_field(name=status[ii]['server_name'], 
                            value=str(status[ii]['player_count']) + "/" + str(status[ii]['max_players']) + " :: " + str(status[ii]['map']), 
                            inline=False)
        else:
            embed.add_field(name="No one is playing",
                            value=":(",
                            inline=False)
            
        await client.send_message(message.channel, embed=embed)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run("TOKEN")