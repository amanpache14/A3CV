function showPreview(event) {
  if (event.target.files.length > 0) {
    var src = URL.createObjectURL(event.target.files[0]);
    var preview = document.getElementById("file-ip-1-preview");
    preview.src = src;
    preview.style.display = "block";
  }
}

function getname () {
  var name = document.getElementById('fileInput'); 
  alert('Selected file: ' + name.files.item(0).name);
};
