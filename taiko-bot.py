import valve.source.master_server
import valve.source.a2s
import discord

# get list of servers, "ip:port"
def get_servers(gamedir):
    servers = []
    with valve.source.master_server.MasterServerQuerier() as msq:
        try:
            for address in msq.find(gamedir=gamedir):
                servers = servers + [str(address[0]) + str(":") + str(address[1])]
        except:
            pass
    return(servers)
# print(get_servers("NeotokyoSource"))

# get info() of single server
def server_status(server):
    try:
        status = dict(
                valve.source.a2s.ServerQuerier((str(server.split(":")[0]), int(server.split(":")[1]))).info()
        )
    except:
        status = 'Timed out waiting for response'
        
    return(status)
# print(server_status('88.150.176.83:26300'))

# create dict of servers and info
def status_dict(servers):
    
    status_d = {}
    
    for server in servers:
        status_d[server] = server_status(server)
        
    # keeps only relevant var, drops timed out servers
    status_d = {k:{l:m for l,m in v.items() if l in 
                 ['server_name', 'map', 'player_count', 'max_players', 'password_protected']} for k,v in status_d.items() 
              if v != 'Timed out waiting for response'}

    # sorts by player count
    status = dict(sorted(status_d.items(), key=lambda x: x[1]['player_count'], reverse = True))

    return(status_d)
print(status_dict(get_servers('NeotokyoSource')))

# converts statuscdict to embed message
def embed(status, desc):
    
    embed = discord.Embed(# title="Title", 
                          description='```css\n'+desc+'```', 
                          color=0xF6B26B if desc == 'All Servers' else 0x00FF00)
    
    # gets status of all servers
    if desc == 'All Servers':
        for server in status.keys():
            embed.add_field(name=':lock: ' + status[server]['server_name'] if status[server]['password_protected'] == 1 \
                            else ':unlock: ' + status[server]['server_name'], 
                            value=str(status[server]['player_count']) + "/" + str(status[server]['max_players']) + " :: " + str(status[server]['map']),
                            inline='False')
     
    # gets status of only active servers
    elif desc == 'Active Servers':
        # checks if any servers with players exist
        if len({k:v for k,v in status.items() if v['player_count'] > 0}.keys()) > 0:
            for server in {k:v for k,v in status.items() if v['player_count'] > 0}.keys():
                embed.add_field(name=':lock: ' + status[server]['server_name'] if status[server]['password_protected'] == 1 \
                                else ':unlock: ' + status[server]['server_name'], 
                                value=str(status[server]['player_count']) + "/" + str(status[server]['max_players']) + " :: " + str(status[server]['map']), 
                                inline='False')
        else:
            embed.add_field(name='No active players on servers', 
                            value=':frowning:')
    
    return(embed)
# print(embed(status, 'All Servers').to_dict())

client = discord.Client()

@client.event
async def on_message(message):
    
    if message.content.startswith('!help'):
        pass
        
    elif message.content.startswith('!all'):
        status_dict(get_servers('NeotokyoSource'))
        await client.send_message(message.channel, embed=embed(status, 'All Servers'))
        
    elif message.content.startswith('!active'):
        status_dict(get_servers('NeotokyoSource'))
        await client.send_message(message.channel, embed=embed(status, 'Active Servers'))
        
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run('NDUzMDY4ODM1MzM2MjI0NzY4.DfbmsQ.w8dp8SOQsfrp9utRVHoKLHG8mHs')