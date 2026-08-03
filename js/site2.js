// =====================================================
// Soderstrand Personal Website
// Shared Components Prototype
// =====================================================

document.addEventListener("DOMContentLoaded", async function () {

    // GitHub Pages repository root
    const siteRoot = "/soderstrand";

    async function loadComponent(id, file) {
        const target = document.getElementById(id);
        if (!target) return;

        try {
            const response = await fetch(siteRoot + "/shared/" + file);

            if (!response.ok) {
                console.error("Unable to load:", siteRoot + "/shared/" + file);
                return;
            }

            target.innerHTML = await response.text();
        } catch (err) {
            console.error("Error loading", file, err);
        }
    }

    await loadComponent("header", "header.html");
    await loadComponent("nav", "nav.html");
    await loadComponent("footer", "footer.html");

    console.log("Shared page components loaded.");
});
