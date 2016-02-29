describe('Main', function () {
    beforeEach(function() {
        loadFixtures('tests.html');
    });

    describe('Tests initialize implementation', function () {
        var requestWasCalled = false;
        var mockRequestFunction = function () { requestWasCalled = true; };
        var mockNavigator = {
            id: {
                request: mockRequestFunction,
                watch: function () {}
            }
        };

        it('Test initialize does not call navigator.id.request', function () {
            Superlists.Accounts.initialize(mockNavigator);
            expect(requestWasCalled).toBeFalsy('check request not called before click');
        });

        it('Test click initializes navigator.id.request', function () {
            Superlists.Accounts.initialize(mockNavigator);
            $('#id_login').trigger('click')
            expect(requestWasCalled).toBeTruthy('check request was called after click');
        });
    });

    describe('Tests for persona implementation', function () {
        var user, token, urls, mockNavigator, requests, xhr;
        beforeEach(function() {
             user = 'current user';
             token = 'csrf token';
             urls = {login : 'login url', logout: 'logout url'};
             mockNavigator = {
                id: {
                    watch: sinon.mock()
                }
            };
            xhr = sinon.useFakeXMLHttpRequest();
            requests = [];
            xhr.onCreate = function (request) { requests.push(request); };
            Superlists.Accounts.initialize(mockNavigator, user, token, urls);
        });
        afterEach(function() {
            mockNavigator.id.watch.reset();
            xhr.restore();
        });
        
        it('Test initialize calls navigator.id.watch', function () {
            expect(mockNavigator.id.watch.calledOnce).toBeTruthy('check watch function called');
        });

        it('Test watch call sees current user', function () {
            var watchCallArgs = mockNavigator.id.watch.firstCall.args[0];
            expect(watchCallArgs.loggedInUser).toMatch(user);
        });

        it('Test onlogin does ajax post to login url', function () {
            var onloginCallback = mockNavigator.id.watch.firstCall.args[0].onlogin;
            onloginCallback();
            expect(requests.length).toEqual(1);
            expect(requests[0].method).toMatch('POST');
            expect(requests[0].url).toMatch(urls.login);
        });

        it('Test onlogin sends assertion with csrf token', function () {
            var onloginCallback = mockNavigator.id.watch.firstCall.args[0].onlogin;
            var assertion = 'browser-id assertion';
            onloginCallback(assertion);
            expect(requests[0].requestBody).toEqual($.param({assertion: assertion, csrfmiddlewaretoken: token}));
        });

        it('Test onlogout function', function () {
            var onlogoutCallback = mockNavigator.id.watch.firstCall.args[0].onlogout;
            expect(typeof onlogoutCallback).toMatch('function');
        });

        it('Test onlogin post failure should do navigator.id.logout', function () {
            mockNavigator.id.logout = sinon.mock();
            var onloginCallback = mockNavigator.id.watch.firstCall.args[0].onlogin;
            var server = sinon.fakeServer.create();
            server.respondWith([403, {}, "permission denied"]);

            onloginCallback();
            expect(mockNavigator.id.logout.called).toBeFalsy('should not logout yet');

            server.respond();
            expect(mockNavigator.id.logout.called).toBeTruthy('should call logout');
        });
    });
});
