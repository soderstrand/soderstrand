// =====================================================
// Soderstrand Personal Website
// Shared Components Prototype
// =====================================================

document.addEventListener("DOMContentLoaded", async function () {

    async function loadComponent(id, file) {
        const target = document.getElementById(id);
        if (!target) return;

        const depth = window.location.pathname.split("/").length - 2;
        const prefix = "../".repeat(Math.max(depth,0));

        const response = await fetch(prefix + "shared/" + file);
        if (!response.ok) {
            console.error("Unable to load " + file);
            return;
        }

        target.innerHTML = await response.text();
    }

    await loadComponent("header","header.html");
    await loadComponent("nav","nav.html");
    await loadComponent("footer","footer.html");

    console.log("Shared page components loaded.");
});
