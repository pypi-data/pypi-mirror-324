
# Introduction

To edit an ONNX model, one common way is to visualize the model graph, and edit it using ONNX Python API. This works fine. However, we have to code to edit, then visualize to check. The two processes may iterate for many times, which is time-consuming. 👋

What if we have a tool, which allows us to **edit and preview the editing effect in a totally visualization fashion**?

Then `onnx-modifier` comes. With it, we can focus on editing the model graph in the visualization pannel. All the editing information will be summarized and processed by Python ONNX API automatically at last. Then our time can be saved! 🚀

`onnx-modifier` is built based on the popular network viewer [Netron](https://github.com/lutzroeder/netron) and the lightweight web application framework [Flask](https://github.com/pallets/flask).

For more information, please refer to [ZhangGe6/onnx-modifier](https://github.com/ZhangGe6/onnx-modifier).