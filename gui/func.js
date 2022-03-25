let settingsButton = document.getElementById("buttonSettings")
let buttonFriendRequests = document.getElementById("buttonFriendRequests")
let buttonAddFriend = document.getElementById("menuAddFriend")
let expandForm = document.getElementById("expandRequestManual")
let goBackHome = document.getElementById("goBackHome")


function hideSettings() {
    let settingsView = document.getElementById("settingsView")
    settingsView.style.display = "none";
}

function hidePendingRequests() {
    let pendingRequestsView = document.getElementById("pendingRequestsView")
    pendingRequestsView.style.display = "none";
}

function hideAddFriend() {
    let sendRequestView = document.getElementById("sendRequestView")
    sendRequestView.style.display = "none";
}

settingsButton.onclick = function() {
    hideAddFriend()
    hidePendingRequests()
    settingsView.style.display = "flex";
};

buttonFriendRequests.onclick = function() {
    hideSettings()
    hideAddFriend()
    pendingRequestsView.style.display = "flex";
}

buttonAddFriend.onclick = function() {
    hideSettings()
    hidePendingRequests()
    sendRequestView.style.display = "flex";
}

expandForm.onclick = function() {

    form = document.getElementById("addFriendFormIP");
    styles = window.getComputedStyle(form)
    if (styles.getPropertyValue('display') == "none") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }

}

function sidebarContactShowDots() {
    document.getElementById("contactDots").setAttribute("style", "display: flex;")
}

function hideContactDots() {
    document.getElementById("contactDots").setAttribute("style", "display: none;")
}

function onContactClick() {
    hideSettings()
    hideAddFriend()
    hidePendingRequests()

    mainViewMenuBar = document.querySelector('#mainViewMenuBar')
    mainViewMenuBar.style.display = "none";

    messagingScreen = document.querySelector('.messaging-screen')

    if (messagingScreen.style.display != "flex") {
        messagingScreen.style.display = "flex";
    }
}

goBackHome.onclick = function() {
    messagingScreen = document.querySelector('.messaging-screen')
    messagingScreen.style.display = "none";

    mainViewMenuBar = document.querySelector('#mainViewMenuBar')
    mainViewMenuBar.style.display = "flex";

}