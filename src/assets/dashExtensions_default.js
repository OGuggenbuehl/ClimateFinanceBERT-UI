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
        }
    }
});