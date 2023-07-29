import React, {Component} from 'react';
import {Otsing} from './Otsing'

export class Avaleht extends Component{

    render(){
        return(
            <div>
                <h1 className='text-centered'>Avaleht</h1>
                <Otsing/>
            </div>
        )
    }
}