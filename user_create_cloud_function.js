const functions = require("firebase-functions");
const admin = require("firebase-admin");

const db = admin.initializeApp(functions.config().firebase).database();

exports.createUser = functions.auth.user().onCreate(async (user) => {
    if (user.email.endsWith("@rice.edu")) {
        await db.ref(`/users/${user.uid}/netId`).set(user.email.split("@")[0]);
        await db.ref(`/users/${user.uid}/name`).set(user.name);
    }
});