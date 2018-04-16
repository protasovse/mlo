let path = require('path');

module.exports = {
    "entry": {
        authorization: "./vue/instances/authorization.js",
        ask_question: "./vue/instances/ask_question.js",
        question: "./vue/instances/question.js",
    },
    "output": {
        "path": path.resolve(__dirname, 'vue', 'bundles'),
        publicPath: '/',
        "filename": "[name].js"
    },

    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader',
            },
            {
                test: /\.js/,
                loader: "babel-loader",
                exclude: /(node_modules|bower_components)/,
            },
            {
                test: /\.css/,
                loader: 'style-loader!css-loader'
            },
            {
                test: /\.less/,
                use: [{
                    loader: "style-loader" // creates style nodes from JS strings
                }, {
                    loader: "css-loader" // translates CSS into CommonJS
                }, {
                    loader: "less-loader" // compiles Less to CSS
                }]
            },
            {
                test: /\.(jpe?g|png|gif|svg)$/i,
                loaders: 'file?name=[path][name].[ext]'
            },
            {
                test: /\.html/,
                loader: 'html-loader'
            }
        ]
    }
};

