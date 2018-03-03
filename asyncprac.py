import bottle


@bottle.route('/')
def index():
    return bottle.static_file('client.html', root='.')

@bottle.route('/r1')
def ndf1():
    print('message from 1')
    return

@bottle.route('/r2')
def ndf2():
    print('message from 2')
    return

if __name__ == '__main__':
    bottle.run(host='localhost', port=8080)#, debug=True)
