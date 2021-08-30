const fonts = ["serif", "sansserif", "monospace"];
const modes = ["lightmode", "sepia", "darkmode"];


function boot() {
    mode = localStorage.getItem("mode");
    if (mode != null){
        document.body.classList.add(mode); 
    }
    //change_mode(mode);

    font = localStorage.getItem("font");
    if (font != null){
    document.body.classList.add(font); 
    }

    }

function change_mode(mode) {
    document.body.classList.remove(modes[0], modes[1], modes[2]);
    // if (document.body.classList != null){
    //     for (let i in modes) {
    //         console.log(modes[i]);
    //         remove(modes[i]);
    //   }}
      document.body.classList.add(mode);
      save("mode", mode)

}


function change_font(clss) {
    document.body.classList.remove(fonts[0], fonts[1], fonts[2]);
    document.body.classList.add(clss);
    save("font", clss);
    }


function remove(clss) {
    document.body.classList.remove(clss);
    }
    
    
function save(key, item){
    
    localStorage.setItem(key, item);
}