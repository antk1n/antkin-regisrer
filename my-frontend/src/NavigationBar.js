/* Navigation bar
*
* importimiseks - import {NavigationBar} from './NavigationBar';
*
* importimiseks - import {Otsing} from './Otsing'
*
* Renderis
* <NavigationBar/>
* 
*/
import React, {Component} from 'react';
import './styles/main.css'

export class NavigationBar extends Component{
    
    render(){
        return(
            <nav className="navbar">
                <a href="/" className="logo-name">
                    Some Fancy Logo
                </a>
                <div
                    className="navbar-menu">
                    <ul>
                        {window.location.pathname !== "/" && <li>
                            <a href="/">Avaleht</a>
                        </li>
                        }
                        {window.location.pathname !== "/create" && <li>
                            <a href="/create">Osaühingu asutamine</a>
                        </li>
                        }
                        {window.location.pathname !== "/help" && <li>
                            <a href="/help">Abi</a>
                        </li>
                        }
                    </ul>
                </div>
            </nav>
        );
    }
}