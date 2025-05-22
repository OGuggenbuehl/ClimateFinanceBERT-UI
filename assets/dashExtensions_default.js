window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, context) {
            const {
                min,
                max,
                colorscale,
                style,
                polyColoring
            } = context.hideout;
            const value = feature.properties[polyColoring];
            if (value === null || value === undefined) {
                style.fillColor = "#A9A9A9";
                return style;
            }
            const normalized = Math.min(Math.max((value - min) / (max - min), 0), 1);
            const color = chroma.scale(colorscale).domain([0, 1])(normalized).hex();
            style.fillColor = color;
            return style;
        },
        function1: function(feature, context) {
            const {
                min,
                max,
                style,
                polyColoring,
                quartile_breaks,
                quartile_colors
            } = context.hideout;
            const value = feature.properties[polyColoring];

            if (value === null || value === undefined) {
                style.fillColor = "#A9A9A9";
                return style;
            }

            // Find which quartile the value belongs to
            let colorIndex = 0;
            for (let i = 1; i < quartile_breaks.length; i++) {
                if (value <= quartile_breaks[i]) {
                    colorIndex = i - 1;
                    break;
                }
            }

            style.fillColor = quartile_colors[colorIndex];
            return style;
        }
    }
});