import './App.css';

import {NavigationBar} from './NavigationBar';
import {Avaleht} from './Avaleht';
import {Create} from './Create';
import {Info} from './Info';
import {Help} from './Help';
import {Edit} from './Edit';

import {BrowserRouter, Route, Routes} from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
    <NavigationBar/>
    <Routes>
      <Route path='/' element={<Avaleht />} exact/>
      <Route path='/create' element={<Create />} exact/>
      <Route path='/help' element={<Help />} exact/>
      <Route path='/info/:id' element={<Info />} exact/>
      <Route path='/edit/:id' element={<Edit />} exact/>
    </Routes>
    </BrowserRouter>
  )
}

export default App;
