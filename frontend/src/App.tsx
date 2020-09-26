import React, {FC} from 'react';
import {Switch, Route, BrowserRouter} from 'react-router-dom';
import Dashboard from "./components/Dashboard";

/**
 * Application root component with routing
 * @constructor FC
 */
const App: FC = () => <div className="padding">
    <BrowserRouter>
        <Switch>
            <Route path="/" component={Dashboard}/>
        </Switch>
    </BrowserRouter>
</div>

export default App;
