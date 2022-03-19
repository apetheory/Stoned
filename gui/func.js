let settingsButton = document.getElementById("buttonSettings")
let buttonFriendRequests = document.getElementById("buttonFriendRequests")

let settingsView = document.getElementById("settingsView")
let pendingRequestsView = document.getElementById("pendingRequestsView")

function hideSettings() {
    settingsView.setAttribute("style", "display: none;")
}

settingsButton.onclick = function() {
    settingsView.setAttribute("style", "display: flex;")
    pendingRequestsView.setAttribute("style", "display:none;")
};

buttonFriendRequests.onclick = function() {
    hideSettings()
        // hide message screen and other elements
    pendingRequestsView.setAttribute("style", "display:flex;")

}