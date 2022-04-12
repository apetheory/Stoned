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

function hideChat() {
    messagingScreen = document.querySelector('.messaging-screen')
    messagingScreen.style.display = "none";
}

function hideDashboard() {
    dashboard = document.querySelector('.dashboardView')
    dashboard.style.display = "none"
}



function showSettings() {
    hideAddFriend()
    hidePendingRequests()
    hideChat()
    hideDashboard()
    mainViewMenuBar = document.querySelector('#mainViewMenuBar')

    if (mainViewMenuBar.style.display == "none") {
        mainViewMenuBar.style.display = "flex";
    }

    settingsView.style.display = "flex";
};

buttonFriendRequests.onclick = function() {
    hideSettings()
    hideAddFriend()
    hideDashboard()
    pendingRequestsView.style.display = "flex";
}

buttonAddFriend.onclick = function() {
    hideSettings()
    hidePendingRequests()
    hideDashboard()
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


goBackHome.onclick = function() {
    messagingScreen = document.querySelector('.messaging-screen')
    messagingScreen.style.display = "none";

    mainViewMenuBar = document.querySelector('#mainViewMenuBar')
    mainViewMenuBar.style.display = "flex";
}

menuDashboard.onclick = function() {
    hideChat()
    hideAddFriend()
    hidePendingRequests()
    hideSettings()

    dashboard = document.querySelector('.dashboardView')
    dashboard.style.display = "flex"

}

function messageBoxKeyPressed(event) {
    if (event.keyCode == 13) {
        sendMessage()
    }
}