const settingsUsernameBox = document.querySelector("#settingsUsernameBox");
const settingsStatusBox = document.querySelector("#settingsStatusBox");
const color1 = document.querySelector("#color1");
const color2 = document.querySelector("#color2");
const color3 = document.querySelector("#color3");
const color4 = document.querySelector("#color4");
const color5 = document.querySelector("#color5");
const color6 = document.querySelector("#color6");
const color7 = document.querySelector("#color7");
const color8 = document.querySelector("#color8");
const color9 = document.querySelector("#color9");
const color10 = document.querySelector("#color10");
const color11 = document.querySelector("#color11");
const settingsServerPort = document.querySelector("#settingsServerPort");

const userProfilePhoto = document.getElementById("userProfilePhoto");
const username = document.querySelectorAll(".username");
const rootVars = document.querySelector(':root');

const addFriendByCodeButton = document.querySelector("#submitFriendRequestCode")


// load settings
eel.expose(loadSettings);

function loadSettings(sf) {
    let settingsFile = JSON.parse(sf);

    // update pfp + username
    userProfilePhoto.src = settingsFile["avatar"];

    for (let i = 0; i < username.length; i++) {
        username[i].innerHTML = settingsFile["username"];
    }

    // Settings tab values
    settingsUsernameBox.value = settingsFile["username"];
    settingsStatusBox.value = settingsFile["status"];
    settingsServerPort.value = settingsFile["internalServerPort"];

    color1.value = settingsFile["colorScheme"]["color1"];
    color2.value = settingsFile["colorScheme"]["color2"];
    color3.value = settingsFile["colorScheme"]["color3"];
    color4.value = settingsFile["colorScheme"]["color4"];
    color5.value = settingsFile["colorScheme"]["color5"];
    color6.value = settingsFile["colorScheme"]["color6"];
    color7.value = settingsFile["colorScheme"]["color7"];
    color8.value = settingsFile["colorScheme"]["color8"];
    color9.value = settingsFile["colorScheme"]["color9"];
    color10.value = settingsFile["colorScheme"]["color10"];
    color11.value = settingsFile["colorScheme"]["color11"];

    rootVars.style.setProperty('--body', color1.value);
    rootVars.style.setProperty('--sidebar-main', color2.value);
    rootVars.style.setProperty('--sidebar-secondary', color3.value);
    rootVars.style.setProperty('--main-font-color', color4.value);
    rootVars.style.setProperty('--secondary-font-color', color5.value);
    rootVars.style.setProperty('--section-title-color', color6.value);
    rootVars.style.setProperty('--section-border-color', color7.value);
    rootVars.style.setProperty('--menu-bar-border', color8.value);
    rootVars.style.setProperty('--status-font-color', color9.value);
    rootVars.style.setProperty('--message-box', color10.value);
    rootVars.style.setProperty('--save-settings-button-border', color11.value);

}

eel.expose(addPendingContact);

function addPendingContact(cF, uid) {

    let clientFile = JSON.parse(cF);

    recvUsername = clientFile["username"]
    recvStatus = clientFile["status"]

    element = "<div class='pending-request-contact' data-uid='" + uid + "'><div class='start'><img src='./res/user.png' /><div class='pending-request-contact-info'><span class='pending-request-contact-username'>" + recvUsername + "</span><spanclass='pending-request-contact-status'>" + recvStatus + "</span></div></div><div class='end'><div class='pending-request-actions'><button data-uid='" + uid + "' class='acceptRequest' onclick='acceptFriendRequest(\"" + uid + "\")'><img src='./res/tick.svg'></button><button data-uid='" + uid + "' class='denyRequest' onclick='denyFriendRequest(\"" + uid + "\")'><img src='./res/x.svg'></button></div></div></div>"

    document.querySelector(".pending-requests").innerHTML += element

}

settingsSubmitBtn.onclick = function() {
    if (settingsUsernameBox.value.length <= 16) {
        let colors = [
            color1.value,
            color2.value,
            color3.value,
            color4.value,
            color5.value,
            color6.value,
            color7.value,
            color8.value,
            color9.value,
            color10.value,
            color11.value
        ]

        let misc = [
            settingsUsernameBox.value,
            settingsStatusBox.value,
            settingsServerPort.value
        ]
        eel.updateSettings(misc, colors)
    }

}

addFriendByCodeButton.onclick = function() {
    friendCode = document.querySelector("#sendFriendRequestCode").value
    eel.addFriend(friendCode)
}

function acceptFriendRequest(destination) {
    let friendRequests = document.querySelectorAll(".pending-request-contact")

    eel.acceptFriendRequest(destination);

    for (let i = 0; i < friendRequests.length; i++) {
        if (friendRequests[i].dataset.uid == destination) {
            friendRequests[i].remove()
        }
    }
}

function denyFriendRequest(destination) {
    let friendRequests = document.querySelectorAll(".pending-request-contact")

    eel.denyFriendRequest(destination);

    for (let i = 0; i < friendRequests.length; i++) {
        if (friendRequests[i].dataset.uid == destination) {
            friendRequests[i].remove()
        }
    }
}

eel.expose(createSidebarContact);

function createSidebarContact(uF, uid) {
    console.log("sfs")
    let userDetails = JSON.parse(uF)

    let contactUsername = userDetails["username"]
    let contactStatus = userDetails["status"]


    let contact = "<div class='sidebar-contact' id='sidebarContact' data-uid=\"" + uid + "\" onmouseover='sidebarContactShowDots()' onmouseleave='hideContactDots()' onclick='onContactClick()'><div class='sidebar-contact-info'><img src='./res/user.png' /><div class='sidebar-contact-user-area'><span id='sidebar-contact-username'>" + contactUsername + "</span><span id='sidebar-contact-status'>" + contactStatus + "</span></div></div><div class='sidebar-dots' id='contactDots'><button id='sidebar-contact-dots' onclick='sidebarContactExpandMenu()'><img src='./res/expand_more_black_24dp.svg' /></button></div>"



    document.querySelector("#sidebar-contacts").innerHTML += contact




}