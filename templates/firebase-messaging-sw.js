importScripts('https://www.gstatic.com/firebasejs/8.0.2/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.0.2/firebase-messaging.js');

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

  messaging.setBackgroundMessageHandler(function(payload) {
    console.log('[firebase-messaging-sw.js] Received background message', payload);
    // Customize notification here
    const notificationTitle = 'Skin Lesion';
    const notificationOptions = {
      body: 'Kindly grant us privilege to send you notifications.',
      icon: '/images/favicon-logo.png'
    };
  
    return self.registration.showNotification(notificationTitle,notificationOptions);
  });
