import './App.css'
import {Outlet, createBrowserRouter} from "react-router-dom"
import Home from './pages/Home'
import Navbar from './components/Navbar'

const AppLayout = ()=> {
  return (
    <>
    <Navbar/>
    <Outlet/>
    </>
  )
}

const router = createBrowserRouter([
  {
    path:"/",
    element:<AppLayout/>,
    children:[
      {
        path:"/",
        element:<Home/>
      }
    ]
  }
])

export default router
