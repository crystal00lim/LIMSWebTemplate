class TinyTree {
    constructor(containerId, data) {
    this.container = document.getElementById(containerId);
    this.data = data;
    this.xmlns = "http://www.w3.org/2000/svg";
    
    this.options = {
      nodeWidth: 100,
      nodeHeight: 60, 
      levelSpacing: 80
    };

    this.initCanvas();

    const resizeObserver = new ResizeObserver(() => {
        this.render(); 
    });
    resizeObserver.observe(this.container);
    }

  initCanvas() {
    this.svg = document.createElementNS(this.xmlns, "svg");
    this.svg.setAttribute("width", "100%");
    this.svg.setAttribute("height", "100%");
    this.svg.style.display = "block";
    
    this.drawGroup = document.createElementNS(this.xmlns, "g");
    this.svg.appendChild(this.drawGroup);
    this.container.appendChild(this.svg);
  }

  render() {
    while (this.drawGroup.firstChild) {
        this.drawGroup.removeChild(this.drawGroup.firstChild);
    }

    const rect = this.container.getBoundingClientRect();
    const width = Math.max(rect.width, 200);
    
    this.drawNode(this.data, width / 2, 20, width / 2, true);
  }

  drawNode(node, x, y, range, isRoot = false) {
    const measureDiv = document.createElement("div");
    measureDiv.innerHTML = node.name;
    measureDiv.style.cssText = `
        display: inline-block;
        padding: 0px;
        font-family: sans-serif;
        font-size: 12px;
        text-align: center;
        line-height: 1.2;
        visibility: hidden;
        position: absolute;
        white-space: nowrap; 
    `;
    document.body.appendChild(measureDiv);

    const padding = 20;
    const boxWidth = measureDiv.offsetWidth + padding;
    const boxHeight = measureDiv.offsetHeight + padding;
    document.body.removeChild(measureDiv);

    if (node.children) {
        const childY = y + this.options.levelSpacing;
        
        const isRootLevel = isRoot && node.children.length === 3;
        const isRectalLevel = !isRoot && node.name === "Rectal" && node.children.length === 3;

        if (isRootLevel) {
            const weights = [0.22, 0.22, 0.56];
            const totalWidth = range * 2;
            const startX = x - range;
            
            let currentOffset = 0;
            node.children.forEach((child, i) => {
                const childAllocatedWidth = totalWidth * weights[i];
                const childX = startX + currentOffset + (childAllocatedWidth / 2);
                
                this.drawCurve(x, y + boxHeight, childX, childY);
                this.drawNode(child, childX, childY, childAllocatedWidth / 2);
                
                currentOffset += childAllocatedWidth;
            });
        } else if (isRectalLevel) {
            // Give SA more space since it's deeper, Mac is a leaf
            const weights = [0.5, 0.2, 0.3];
            const totalWidth = range * 2;
            const startX = x - range;

            let currentOffset = 0;
            node.children.forEach((child, i) => {
                const childAllocatedWidth = totalWidth * weights[i];
                const childX = startX + currentOffset + (childAllocatedWidth / 2);
                
                this.drawCurve(x, y + boxHeight, childX, childY);
                this.drawNode(child, childX, childY, childAllocatedWidth / 2);
                
                currentOffset += childAllocatedWidth;
            });
        } else {
            const step = (range * 2) / node.children.length;
            node.children.forEach((child, i) => {
                const childX = (x - range) + (step * i) + (step / 2);
                this.drawCurve(x, y + boxHeight, childX, childY);
                this.drawNode(child, childX, childY, step / 2);
            });
        }
    }

    const rect = document.createElementNS(this.xmlns, "rect");
    rect.setAttribute("x", x - boxWidth / 2);
    rect.setAttribute("y", y);
    rect.setAttribute("width", boxWidth);
    rect.setAttribute("height", boxHeight);
    rect.setAttribute("fill", "white");
    rect.setAttribute("stroke", "#333");
    rect.setAttribute("rx", "4");
    this.drawGroup.appendChild(rect);

    const foreignObject = document.createElementNS(this.xmlns, "foreignObject");
    foreignObject.setAttribute("x", x - boxWidth / 2);
    foreignObject.setAttribute("y", y);
    foreignObject.setAttribute("width", boxWidth);
    foreignObject.setAttribute("height", boxHeight);

    const div = document.createElement("div");
    div.innerHTML = node.name; 
    div.setAttribute("style", `
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
        font-family: sans-serif;
        font-size: 12px;
        text-align: center;
        line-height: 1.2;
        color: #333;
    `);

    foreignObject.appendChild(div);
    this.drawGroup.appendChild(foreignObject);
  }

  drawCurve(sx, sy, ex, ey) {
    const path = document.createElementNS(this.xmlns, "path");
    const my = (sy + ey) / 2;
    const d = `M${sx},${sy} C${sx},${my} ${ex},${my} ${ex},${ey}`;
    path.setAttribute("d", d);
    path.setAttribute("stroke", "#ccc");
    path.setAttribute("fill", "none");
    this.drawGroup.insertBefore(path, this.drawGroup.firstChild);
  }
}

window.addEventListener('DOMContentLoaded', () => {
    const dataElement = document.getElementById('my-data-json');
    if (dataElement) {
        const rawData = JSON.parse(dataElement.textContent);
        new TinyTree("tree-container", rawData);
    }
});