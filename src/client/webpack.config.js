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

var configReviewBurger = Object.assign({}, config, {
    name: "configReviewBurger",
    entry: "./js/review_burger.js",
    output: {
        path: __dirname + "../../static/",
        publicPath: "../static/",
        filename: "../static/js/app.review_burger.min.js",
        library: 'publicApp',
        libraryTarget: 'window'
    },
    devtool: 'eval-source-map',
    resolve:  { 
        alias: {
            'vue': 'vue/dist/vue.esm-bundler.js' // 'vue/dist/vue.common.js' for webpack 1
        }
    },
    plugins: [
    // Define Bundler Build Feature Flags
    new webpack.DefinePlugin({
        // Drop Options API from bundle
        __VUE_OPTIONS_API__: false,
        __VUE_PROD_DEVTOOLS__: false,
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__ : false
      }),
    ]
});

// Return Array of Configurations
module.exports = [configReviewBurger];