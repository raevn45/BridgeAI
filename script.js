// BridgeAI Frontend Script


document.addEventListener(
    "DOMContentLoaded",
    () => {


        console.log("BridgeAI initialized");



        const textarea = document.querySelector("textarea");


        if (textarea) {


            textarea.addEventListener(
                "focus",
                () => {

                    textarea.style.boxShadow =
                    "0 0 35px rgba(34,211,238,0.5)";

                }
            );



            textarea.addEventListener(
                "blur",
                () => {

                    textarea.style.boxShadow =
                    "none";

                }
            );


        }





        const button =
        document.querySelector("button");



        if(button){


            button.addEventListener(
                "click",
                () => {


                    button.innerHTML =
                    "◌ Processing...";


                }
            );


        }





        const upload =
        document.querySelector(
            'input[type="file"]'
        );



        if(upload){


            upload.addEventListener(
                "change",
                () => {


                    if(upload.files.length > 0){


                        upload.parentElement.style.border =
                        "1px solid #22d3ee";



                        upload.parentElement.querySelector("label").innerHTML =
                        "✓ " + upload.files[0].name;


                    }


                }
            );


        }



    }
);