(function () {
    var validModes = ["light", "sunrise", "sunset", "dark"];
    var modeLabels = {
        light: "Light",
        sunrise: "Sunrise",
        sunset: "Sunset",
        dark: "Dark",
    };
    var modeIcons = {
        light: String.fromCodePoint(9728),
        sunrise: String.fromCodePoint(10040),
        sunset: String.fromCodePoint(9730),
        dark: String.fromCodePoint(9733),
    };

    function getCurrentMode() {
        var current = document.documentElement.getAttribute("data-theme");
        if (current && validModes.includes(current)) {
            return current;
        }
        return "light";
    }

    function updateThemeUI(mode) {
        var currentMode = modeLabels[mode] || "Light";
        var currentIcon = modeIcons[mode] || modeIcons.light;
        var cycleLink = document.getElementById("theme-cycle");
        var cycleIcon = document.getElementById("theme-cycle-icon");

        if (cycleIcon) {
            cycleIcon.textContent = currentIcon;
        }

        if (cycleLink) {
            cycleLink.setAttribute(
                "title",
                "Current mode: " + currentMode + ". Activate to cycle theme",
            );
            cycleLink.setAttribute(
                "aria-label",
                "Current mode " +
                    currentMode.toLowerCase() +
                    ". Activate to cycle theme",
            );
        }
    }

    function setTheme(mode) {
        if (!validModes.includes(mode)) {
            return;
        }

        document.documentElement.setAttribute("data-theme", mode);
        document.documentElement.classList.remove(
            "dark-mode",
            "light-mode",
            "sunrise-mode",
            "sunset-mode",
        );
        document.documentElement.classList.add(mode + "-mode");
        updateThemeUI(mode);
    }

    function cycleTheme() {
        var current = getCurrentMode();
        var nextIdx = (validModes.indexOf(current) + 1) % validModes.length;
        var next = validModes[nextIdx];
        setTheme(next);
        localStorage.setItem("theme", next);
    }

    function bindThemeCycleLink() {
        var cycleLink = document.getElementById("theme-cycle");
        if (!cycleLink) {
            return;
        }

        cycleLink.addEventListener("click", function (e) {
            e.preventDefault();
            cycleTheme();
        });

        cycleLink.addEventListener("keydown", function (e) {
            if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                cycleTheme();
            }
        });

        updateThemeUI(getCurrentMode());
    }

    function bindAsteriskToggle() {
        var asterisk = document.getElementById("top");
        if (!asterisk) {
            return;
        }

        asterisk.addEventListener("click", function () {
            cycleTheme();
        });

        asterisk.addEventListener("keydown", function (e) {
            if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                cycleTheme();
            }
        });
    }

    function initThemeControls() {
        bindThemeCycleLink();
        bindAsteriskToggle();
        updateThemeUI(getCurrentMode());
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initThemeControls, {
            once: true,
        });
    } else {
        initThemeControls();
    }
})();
