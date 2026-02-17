
import React from "react";
import { useState } from "react";
const scratch_book_1 =()=>{
    const [fakePassword, setFakePassword] = useState(6)
    const [helloWorldResponds, setHelloWorldResponds] = useState("")
    const [helloWorldRestful, setHelloWorldRestfulResponds] = useState("")

    async function  handleHelloWorld (){
        const url = "http://127.0.0.1:5000/hello"
    
        try{
            const response = await fetch (url)
            if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
            }

            const result = await response.json();
            
            setHelloWorldResponds(result.content)
            
        }catch(e){
            console.error(e.message)
        }
    }

    async function handleHelloWorld_Restful(){
        const url = `http://127.0.0.1:5000/hello_restful/${fakePassword}`

        try{
            const response = await fetch (url)
            if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
            }

            const result = await response.json();
            
            setHelloWorldRestfulResponds(result.content + result.content)

        }catch(e){
            console.error(e.message)
        }
    }

    return(
        <div>
            <div>
                <button onClick={handleHelloWorld}>Hello World</button>
            </div>
            <div>
                <p>Input Your Password Fake!</p>
                <input
                    placeholder="password"
                    type="number"
                    value={fakePassword}
                    onChange={(e) => setFakePassword(Number(e.target.value))}
                />
                <button onClick={handleHelloWorld_Restful}>Hello World with RestFul</button>
            </div>
            <div>
                <p>Response from Hello World: {helloWorldResponds}</p>
                <p>Response from Hello World Restful:{helloWorldRestful}</p>
            </div>
        </div>
    )
}