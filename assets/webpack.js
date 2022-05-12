var path = require("path");
var webpack = require('webpack')
var BundleTracker = require("webpack-bundle-tracker");

module.exports = {
    mode: "development",
    context: __dirname,
    entry:  {
        calendar: './src/calendar/index.js',
        ui: './src/widgets/index.js'
    },
    output: {
        path: path.resolve('./bundles/'),
        filename: '[name].js'
    },
    plugins: [
        new BundleTracker({filename: './webpack-stats.json'})
    ],
    module: {
        rules: [
            {
                test: /\.css$/,
                'loader': 'style-loader'
            },
            {
                test: /\.css$/,
                loader: 'css-loader',
                options: {
                    modules: true,
                   
                }
            },
            {
                test: /\.js$/,
                loader: 'babel-loader',
                exclude: /node_modules/,
                options: {
                    presets: [
                        "@babel/preset-env",
                        "@babel/preset-react"
                    ]
                }
            }
        ]
    },
    resolve: {
        extensions: [ '.js', '.jsx', '.css']
    },
}