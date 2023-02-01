<?php
$target_dir = "uploads/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));
if($imageFileType != "pdf" && $imageFileType != "zip" ) {
    echo "Sorry, only PDF and ZIP files are allowed.";
    $uploadOk = 0;
}
// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
    echo "Sorry, your file was not uploaded.";
// if everything is ok, try to upload file
} else {
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
        $name = explode(".",basename($target_file))[0];

        $command = escapeshellcmd('python ./konwerter.py '.basename($target_file).' '.$name.'.csv');
        $output = shell_exec($command);
        $namecsv=$name.".csv";
        header("Content-type:application/csv");
        header('Content-Disposition: attachment; filename="'.$namecsv.'";');
        readfile($name.".csv");
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
}
?>


