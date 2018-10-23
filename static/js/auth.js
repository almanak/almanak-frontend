// Auth0 vars
var lock_options = {
  language: "da",
  title: "Log ind",
  closable: true,
  container: 'auth0-container',
  // forgotPasswordLink: '{{env.AUTH0_FORGOT_URL}}',
  avatar: null,
  theme: {
    logo: null,
  },
  auth: {
    redirectUrl: "{{env.AUTH0_CALLBACK_URL}}",
    responseType: 'code',
    params: {
      scope: 'openid email',
      // used to store return_ul, which is stored in the hash-value - BAD CHOICE ACTUALLY!
      state: window.btoa(window.location.hash)
    }
  },
  additionalSignUpFields: [{
    name: "brugernavn",
    placeholder: "Indtast brugernavn",
    // The following properties are optional
    validator: function(brugernavn) {
      return {
         valid: brugernavn.length >= 3 && brugernavn.length <= 40,
         hint: "Minimum 3 karakterer"
      };
    }
  }]
};

var lock = new Auth0Lock("{{env.AUTH0_CLIENT_ID}}", "{{env.AUTH0_DOMAIN}}", lock_options);
  // lock.show();

  // lock.on('authenticated', function(authResult) {
  //   console.log(authResult);
  // });
