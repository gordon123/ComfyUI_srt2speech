// comfyui_subtitle_ui.js

// Register a custom UI renderer for our node
app.ui.registerCustomNodeUI("GetSubtitleByIndex", async (node, app) => {
    // Create elements to display subtitle info
    const container = document.createElement("div");
    container.style.padding = "8px";
    container.style.borderTop = "1px solid #333";
    container.style.marginTop = "6px";
  
    const textLabel = document.createElement("div");
    textLabel.style.fontWeight = "bold";
    textLabel.innerText = "▶️ Subtitle";
    const textContent = document.createElement("pre");
    textContent.style.whiteSpace = "pre-wrap";
    textContent.style.color = "#ccc";
    container.appendChild(textLabel);
    container.appendChild(textContent);
  
    const timeLabel = document.createElement("div");
    timeLabel.style.fontWeight = "bold";
    timeLabel.style.marginTop = "8px";
    timeLabel.innerText = "⏱ Timestamp";
    const timeContent = document.createElement("div");
    timeContent.style.color = "#ccc";
    container.appendChild(timeLabel);
    container.appendChild(timeContent);
  
    const allLabel = document.createElement("div");
    allLabel.style.fontWeight = "bold";
    allLabel.style.marginTop = "8px";
    allLabel.innerText = "📜 All Subtitles";
    const allContent = document.createElement("pre");
    allContent.style.maxHeight = "160px";
    allContent.style.overflowY = "auto";
    allContent.style.whiteSpace = "pre-wrap";
    allContent.style.color = "#ccc";
    container.appendChild(allLabel);
    container.appendChild(allContent);
  
    const timeListLabel = document.createElement("div");
    timeListLabel.style.fontWeight = "bold";
    timeListLabel.style.marginTop = "8px";
    timeListLabel.innerText = "⏰ All Timestamps";
    const timeListContent = document.createElement("pre");
    timeListContent.style.maxHeight = "160px";
    timeListContent.style.overflowY = "auto";
    timeListContent.style.whiteSpace = "pre-wrap";
    timeListContent.style.color = "#ccc";
    container.appendChild(timeListLabel);
    container.appendChild(timeListContent);
  
    // Append UI to the node
    node.appendChild(container);
  
    // Auto update on execution
    node.addEventListener("execution", () => {
      const outputs = app.graph.outputs[node.id];
      if (!outputs || !outputs[0]) return;
  
      textContent.textContent = outputs[0];
      timeContent.textContent = outputs[1];
      allContent.textContent = outputs[2];
      timeListContent.textContent = outputs[3];
    });
  });
  
  // ✅ node class
NODE_CLASS_BUTTONS = NODE_CLASS_BUTTONS || {};
NODE_CLASS_BUTTONS["GetSubtitleByIndex"] = {
  all_subtitles: { name: "📋 All Subtitles", type: "output" },
  all_timestamps: { name: "⏱️ All Timestamps", type: "output" }
};