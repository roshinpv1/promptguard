const path = require("path");
const webpack = require("webpack");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const ModuleFederationPlugin = require("webpack/lib/container/ModuleFederationPlugin");

module.exports = {
  entry: "./src/index.tsx",
  mode: "development",
  devServer: {
    port: 3000,
    historyApiFallback: true,
    hot: true,
    headers: {
      "Access-Control-Allow-Origin": "*",
    },
  },
  resolve: {
    extensions: [".tsx", ".ts", ".jsx", ".js"],
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: {
          loader: "ts-loader",
          options: {
            transpileOnly: true,
            compilerOptions: {
              noEmit: false,
            },
          },
        },
        exclude: /node_modules/,
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
  plugins: [
    new webpack.DefinePlugin({
      "process.env.REACT_APP_API_URL": JSON.stringify(
        process.env.REACT_APP_API_URL || "http://localhost:8000"
      ),
    }),
    new ModuleFederationPlugin({
      name: "promptshield_host",
      remotes: {},
      exposes: {
        "./ScanDashboard": "./src/pages/ScanDashboard",
        "./APITester": "./src/pages/APITester",
        "./ResultsViewer": "./src/pages/ResultsViewer",
        "./ConfigEditor": "./src/pages/ConfigEditor",
      },
      shared: {
        react: {
          singleton: true,
          requiredVersion: "^18.2.0",
          eager: true,
        },
        "react-dom": {
          singleton: true,
          requiredVersion: "^18.2.0",
          eager: true,
        },
      },
    }),
    new HtmlWebpackPlugin({
      template: "./public/index.html",
    }),
  ],
};

