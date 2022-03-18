function goToMainMenu() {
    console.log("test")
    let settings_view = document.getElementById("settings")
    settings_view.setAttribute("style", "display: none;")

    let main_view = document.getElementById("home")
    main_view.setAttribute("style", "display: flex;")
}


function goToSettings() {
    let settings_view = document.getElementById("settings")
    settings_view.setAttribute("style", "display: flex;")

    let main_view = document.getElementById("home")
    main_view.setAttribute("style", "display: none;")
}