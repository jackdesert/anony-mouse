const AVAILABLE = 0
const RESERVED = 1
const RESERVED_BY_YOU = 2
const WAITING = 3

var page = new Vue(
    {
        el: '#container',
        data: {composeVisible: false,
               message: '',
               state: null,
               token: null},
        methods: {
            showAvailable: function(event){
                return this.state === AVAILABLE
            },
            showReserved: function(event){
                return this.state === RESERVED
            },
            showReservedByYou: function(event){
                return this.state === RESERVED_BY_YOU
            },
            showWaiting: function(event){
                return this.state === WAITING
            },
            reserve: function(event) {
                // See http://youmightnotneedjquery.com

                const request = new XMLHttpRequest()
                const that = this

                request.open('GET', '/reserve', true)
                request.setRequestHeader('Content-Type', 'application/json')

                request.onload = function() {
                    if (request.status >= 200 && request.status < 400) {
                        // Success!
                        var resp = request.responseText
                        var data = JSON.parse(resp)
                        if (data.token){
                            // Presence of a token indicates success
                            console.log('found a token')
                            console.log('setting state to ', data.state)
                            that.token = data.token
                            that.state = data.state
                            // Note we are not setting that.state because
                            // "reserved by me" and "reserved by someone else"
                            // have two different meanings

                            // TODO close compose window after time elapses
                        }else{
                            // No token means somebody else has this reserved
                            that.state = data.state
                        }

                    } else {
                        // We reached our target server, but it returned an error
                        console.log('ERROR Reserve')

                    }
                }

                request.onerror = function() {
                    // There was a connection error of some sort
                        console.log('BIGERROR Reserve')
                }

                request.send()
            },
            stopCompose: function(event) {
                alert('need method for cancel reservation')
            },
            publish: function(event) {
                // See http://youmightnotneedjquery.com

                const request = new XMLHttpRequest()
                const data = {'message': this.message, token: this.token}

                request.open('POST', '/publish', true)
                request.setRequestHeader('Content-Type', 'application/json')


                request.onload = function() {
                    if (request.status >= 200 && request.status < 400) {
                        // Success!
                        var resp = request.responseText
                        console.log('SUCCESS')
                        console.log(request)
                    } else {
                        // We reached our target server, but it returned an error
                        console.log('ERROR')
                        console.log(request)

                    }
                }

                request.onerror = function() {
                    // There was a connection error of some sort
                        console.log('BIGERROR')
                }

                request.send(JSON.stringify(data))

            },
            poll: function(event) {
                // See http://youmightnotneedjquery.com

                const request = new XMLHttpRequest()
                const data = {'token': this.token}
                const that = this

                request.open('POST', '/state', true)
                request.setRequestHeader('Content-Type', 'application/json')


                request.onload = function() {
                    if (request.status >= 200 && request.status < 400) {
                        // Success!
                        console.log('SUCCESS poll')
                        const resp = request.responseText
                        const state = JSON.parse(resp).state
                        console.log('Setting state to ', state)
                        that.state = state
                    } else {
                        // We reached our target server, but it returned an error
                        console.log('ERROR poll')
                        console.log(request)

                    }
                }

                request.onerror = function() {
                    // There was a connection error of some sort
                        console.log('BIGERROR poll')
                }

                request.send(JSON.stringify(data))

            }

        }

    }
)


// Show things that were hidded during load
document.querySelectorAll('.hide-on-load').forEach(function(item, index, array){
    item.classList.remove('hide-on-load')
})

page.poll()
