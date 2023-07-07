// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyC7A6GSBWXsqAiPD4v-HnyZAIiJ4waBqAA",
  authDomain: "lovefi-b5d8f.firebaseapp.com",
  projectId: "lovefi-b5d8f",
  storageBucket: "lovefi-b5d8f.appspot.com",
  messagingSenderId: "2278232401",
  appId: "1:2278232401:web:a9a22f2d9cd5949af60370",
  // measurementId: "G-YQJDGCMWGV"
};

// Initialize Firebase
export const firebaseApp = initializeApp(firebaseConfig);
export const firestoreDb = getFirestore(firebaseApp);