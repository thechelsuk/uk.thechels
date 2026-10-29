// Colour themes: sunrise, day, sunset, night, or "system".
// "system" (nothing saved) follows the device: dark -> night, otherwise day.
// The inline script in _includes/header.html applies the theme before paint;
// this file wires up the header picker, the title asterisk and the footer avatar.
(function () {
    var KEY = "theme";
    var MODES = ["sunrise", "day", "sunset", "night"];
    var LABELS = { sunrise: "Sunrise", day: "Day", sunset: "Sunset", night: "Night" };
    var ICONS = { sunrise: "◑", day: "◒", sunset: "◑", night: "◒" };
    var root = document.documentElement;
    var darkQuery = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;

    function storedChoice() {
        var value = null;
        try { value = localStorage.getItem(KEY); } catch (e) { /* storage blocked */ }
        return MODES.indexOf(value) > -1 ? value : "system";
    }

    function resolve(choice) {
        if (MODES.indexOf(choice) > -1) return choice;
        return darkQuery && darkQuery.matches ? "night" : "day";
    }

    function apply(choice) {
        var mode = resolve(choice);
        root.setAttribute("data-theme", mode);
        MODES.forEach(function (m) { root.classList.toggle(m + "-mode", m === mode); });

        var buttons = document.querySelectorAll("[data-theme-choice]");
        for (var i = 0; i < buttons.length; i++) {
            buttons[i].setAttribute("aria-pressed", String(buttons[i].getAttribute("data-theme-choice") === choice));
        }

        // Footer avatar link and icon (they cycle the themes).
        var cycleIcon = document.getElementById("theme-cycle-icon");
        if (cycleIcon) cycleIcon.textContent = ICONS[mode];
        var cycleLink = document.getElementById("theme-cycle");
        if (cycleLink) {
            cycleLink.setAttribute("title", "Current theme: " + LABELS[mode] + ". Activate to cycle theme");
            cycleLink.setAttribute("aria-label", "Current theme " + mode + ". Activate to cycle theme");
        }
    }

    function choose(choice) {
        try {
            if (choice === "system") localStorage.removeItem(KEY);
            else localStorage.setItem(KEY, choice);
        } catch (e) { /* storage blocked: still switch for this page */ }
        apply(choice);
    }

    function cycle() {
        var current = resolve(storedChoice());
        choose(MODES[(MODES.indexOf(current) + 1) % MODES.length]);
    }

    function init() {
        apply(storedChoice());

        document.addEventListener("click", function (e) {
            var button = e.target.closest("[data-theme-choice]");
            if (button) {
                choose(button.getAttribute("data-theme-choice"));
                return;
            }
            if (e.target.closest("#top, #theme-cycle")) {
                e.preventDefault();
                cycle();
            }
        });

        document.addEventListener("keydown", function (e) {
            if ((e.key === "Enter" || e.key === " ") && e.target.closest && e.target.closest("#top")) {
                e.preventDefault();
                cycle();
            }
        });

        // While on "system", follow the device switching light/dark.
        if (darkQuery) {
            var onChange = function () { if (storedChoice() === "system") apply("system"); };
            if (darkQuery.addEventListener) darkQuery.addEventListener("change", onChange);
            else if (darkQuery.addListener) darkQuery.addListener(onChange);
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init, { once: true });
    } else {
        init();
    }
})();
