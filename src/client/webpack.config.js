const webpack = require("webpack");

// common settings
var config = {
    watch: true,
    module: {
        rules: [            
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: ["babel-loader"]
            },

            {
                test: /\.(sa|sc|c)ss$/,
                use: []
            }
        ]
    },
    resolve: {
        extensions: ["*", ".js", ".jsx"]
    }
};

var configLoggedIn = Object.assign({}, config, {
    name: "configLoggedIn",
    entry: "./js/logged_in.js",
    output: {
        path: __dirname + "../../src/static/",
        publicPath: "../../src/static/",
        filename: "../../src/static/js/app.loggedin.min.js",
        library: 'publicApp',
        libraryTarget: 'window'
    },
    devtool: 'eval-source-map',
    resolve:  { 
        alias: {
            'vue': 'vue/dist/vue.esm.js' // 'vue/dist/vue.common.js' for webpack 1
        }
    },
    plugins: [
    ]
});

// Return Array of Configurations
module.exports = [configLoggedIn];