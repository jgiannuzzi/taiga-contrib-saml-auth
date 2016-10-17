AUTH_URL = "/saml/initiate-login/"

SamlLoginButtonDirective = ($window, $params, $location, $config, $events, $confirm,
                              $auth, $navUrls, $loader) ->
    # Login or register a user with SAML.
    #
    # Example:
    #     tg-saml-login-button()
    #
    # Requirements:
    #   - ...

    link = ($scope, $el, $attrs) ->
        loginOnSuccess = (response) ->
            if $params.next and $params.next != $navUrls.resolve("login")
                nextUrl = $params.next
            else
                nextUrl = $navUrls.resolve("home")

            $events.setupConnection()

            $location.search("next", null)
            $location.search("token", null)
            $location.search("state", null)
            $location.path(nextUrl)

        loginOnError = (response) ->
            $location.search("state", null)
            $loader.pageLoaded()

            if response.data._error_message
                $confirm.notify("light-error", response.data._error_message )
            else
                $confirm.notify("light-error", "Our Oompa Loompas have not been able to get your
                                                credentials with SAML.")  #TODO: i18n

        loginWithSamlAccount = ->
            type = $params.state
            token = $params.token

            return if not (type == "saml")
            $loader.start(true)

            data = {token: token}
            $auth.login(data, type).then(loginOnSuccess, loginOnError)

        loginWithSamlAccount()

        $el.on "click", ".button-auth", (event) ->
            redirectToUri = $location.absUrl()
            url = "#{AUTH_URL}?next=#{redirectToUri}"
            $window.location.href = url

        $scope.$on "$destroy", ->
            $el.off()

    return {
        link: link
        restrict: "EA"
        template: ""
    }

module = angular.module('taigaContrib.samlAuth', [])
module.directive("tgSamlLoginButton", ["$window", '$routeParams', "$tgLocation", "$tgConfig", "$tgEvents",
                                         "$tgConfirm", "$tgAuth", "$tgNavUrls", "tgLoader",
                                         SamlLoginButtonDirective])
