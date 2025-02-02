import {RegisterImportPool, DynDep} from "./Base";

let ex; const exModulePromises = ex = {
    u: import(/* webpackChunkName: "LinoUtils_EventManager" */"./LinoUtils")
}

class EventManager extends DynDep {

}
