const AVAILABLE = 0
const RESERVED = 1
const RESERVED_BY_YOU = 2
const WAITING = 3

const POLL_PERIOD_MS = 5000

// Use custom delimiters so jinja2 and vue.js can work together
const DELIMITERS = ['${', '}']

var page = new Vue(
    {
        el: '#container',
        delimiters: DELIMITERS,
        data: {composeVisible: false,
               message: '',
               state: null,
               token: null,
               blah: [1,3,2,5,3,3,3,3,3,3],
               themes: {},
               selectedTheme: 1,
        },
        methods: {
            showAvailable: function(event){
                'use strict'
                return this.state === AVAILABLE
            },
            showReserved: function(event){
                'use strict'
                return this.state === RESERVED
            },
            showReservedByYou: function(event){
                'use strict'
                return this.state === RESERVED_BY_YOU
            },
            showWaiting: function(event){
                'use strict'
                return this.state === WAITING
            },
            reserve: function(event) {
                'use strict'
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
                'use strict'
                alert('need method for cancel reservation')
            },
            publish: function(event) {
                'use strict'
                // See http://youmightnotneedjquery.com

                const request = new XMLHttpRequest()
                const data = {'message': this.message,
                              token: this.token,
                              theme_index: this.selectedTheme}
                const that = this

                request.open('POST', '/publish', true)
                request.setRequestHeader('Content-Type', 'application/json')


                request.onload = function() {
                    if (request.status >= 200 && request.status < 400) {
                        // Success!
                        var resp = request.responseText
                        var blob = JSON.parse(resp)
                        console.log('SUCCESS')
                        console.log(request)
                        // Set state to hide compose window
                        that.state = blob.state
                        // Reset message
                        that.message = ''
                        alert('Success!')
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
                'use strict'
                // Poll periodically
                setTimeout(this.poll, POLL_PERIOD_MS)

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
                        const blob = JSON.parse(request.responseText)
                        const state = blob.state
                        const secondsRemaining = blob.seconds_remaining
                        console.log('Setting state to ', state)
                        that.state = state

                        console.log('Seconds Remaining: ', secondsRemaining)
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
    'use strict'
    item.classList.remove('hide-on-load')
})

page.themes = THEMES
page.poll()
