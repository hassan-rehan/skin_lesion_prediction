const firebaseConfig = {
    apiKey: "AIzaSyCDvirvL7ZL1EewpMpHjThYtCvANYMkdL4",
    authDomain: "skin-lesion-bfd75.firebaseapp.com",
    databaseURL: "https://skin-lesion-bfd75.firebaseio.com",
    projectId: "skin-lesion-bfd75",
    storageBucket: "skin-lesion-bfd75.appspot.com",
    messagingSenderId: "273006946923",
    appId: "1:273006946923:web:6a2df015917d2320875f2e",
    measurementId: "G-HPSCYW3FF4"
  };

  firebase.initializeApp(firebaseConfig);


  
  const messaging = firebase.messaging();
  messaging.usePublicVapidKey("BC1qI-n3sCKaMEtijMRR9rytD8i3QayU-FXSeQjMUM4b0GgUu5TZhmEcC17yYOYEx0FYqhkwZ_lC1dqaS8gHb_o");

  // Retrieve Firebase Messaging object.

    messaging.requestPermission().then(function() {
    console.log('Notification permission granted.');
    console.log(messaging.getToken());
    return messaging.getToken();
    // ...
    }).then(function(token) {
        $('#fcm_token').val(token);
        // ...
        }).catch(function(err) {
    console.log('Unable to get permission to notify.', err);
    });


    messaging.onMessage((payload) => {
        console.log('Message received. ', payload);
        $('.number-alert').empty().html(payload.data['badge']);
        $('.number-message').empty().html('You have '+payload.data['badge']+' messages.');
      });
      
    messaging.onTokenRefresh(function () {
      messaging.getToken()
      .then(function(newToken){
        console.log("New Token : "+ newToken);
        sendToServer(newToken);
      })
      .catch(function(reason){
        console.log(reason);
      })
    });

    function sendToServer(token){
      $.ajax({
        url : "{% url 'update_fcm_token' %}",
        type : "POST",
        data : {fcm_token : token}
      }).done(function(response){
        if(response == "True"){
          console.log("FCM token updated.")
        }
        else{
          console.log("Error while updating FCM token.")
        }
      });
    }