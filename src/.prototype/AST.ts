import {
    TArgType,
    TArgReturn,
    TArgValue,
    IArgProps,
    IArgElement,
    TInstructionType,
    IInstructionProps,
    ISyntaxElement,
    IStack,
    IAST
} from "./@types/AST";

// ---- Argument Element ---------------------------------------------------------------------------

class ArgElement implements IArgElement {
    private _argType: TArgType;
    private _returnType: TArgReturn;
    private _argName: string;
    private _args: IArgElement[] | null;
    private _value: TArgValue | null;

    constructor(argType: TArgType, returnType: TArgReturn, props: IArgProps) {
        const { argName, args, value } = { ...props };

        switch (argType) {
            case "function":
                if (!this._validateArgType("function", argName)) {
                    throw Error(`Invalid argument type: "${argName}" is not a function`);
                }
                if (args === undefined) {
                    throw Error(`Invalid arguments: "${argName}" requires arguments`);
                } else {
                    try {
                        this._args = this._validateArgs(argName, args);
                    } catch (e) {
                        throw e;
                    }
                }
                if (value !== undefined) {
                    console.warn(`"${argName}" is a function and doesn't store a value`);
                }
                this._value = null;
                break;
            case "value":
                if (!this._validateArgType("value", argName)) {
                    throw Error(`Invalid argument type: "${argName}" is not a value`);
                }
                if (args !== undefined) {
                    console.warn(`"${argName}" is a value and doesn't take arguments`);
                }
                this._args = null;
                if (value === undefined) {
                    throw Error("Invalid argument value: value is required");
                }
                this._value = value;
                break;
            default:
                throw Error(`Invalid argument type: "${argType}" type doesn't exist`);
        }

        this._argType = argType;
        this._returnType = returnType;
        this._argName = argName;
    }

    private _validateArgType(type: TArgType, argName: string): boolean {
        return true;
    }

    private _validateArgs(argName: string, args: IArgElement[]): IArgElement[] {
        // throw Error(`Invalid arguments: .....`);
        return args;
    }

    /** Returns the argument element type - function or value. */
    get argType() {
        return this._argType;
    }

    /** Returns the return type of the argument element. */
    get returnType() {
        return this._returnType;
    }

    /** Returns the state properties of the argument element. */
    get props() {
        const propObj: IArgProps = { argName: this._argName };
        if (this._args) {
            propObj["args"] = this._args;
        }
        if (this._value) {
            propObj["value"] = this._value;
        }
        return propObj;
    }
}

// ---- Syntax Element - instruction ---------------------------------------------------------------

class SyntaxElement implements ISyntaxElement {
    private _type: TInstructionType;
    private _instruction: string;
    private _args: IArgElement[] | null;
    private _childStack: ISyntaxElement[] | null;

    constructor(type: TInstructionType, props: IInstructionProps) {
        const { instruction, args, childStack } = { ...props };
        this._instruction = instruction;

        switch (type) {
            case "start":
                if (instruction !== "start") {
                    console.warn('instruction for "start" should be "start"');
                }
                this._instruction = "start";
                if (args !== undefined) {
                    console.warn('"start" takes no arguments');
                }
                this._args = null;
                if (childStack === undefined) {
                    console.warn('"start" takes a child flow');
                    this._childStack = [];
                } else {
                    this._childStack = childStack;
                }
                break;
            case "action":
                if (instruction !== "action") {
                    console.warn('instruction for "action" should be "action"');
                }
                this._instruction = "action";
                if (args === undefined) {
                    throw Error('Invalid arguments: "action" requires an argument');
                }
                this._args = args;
                if (childStack === undefined) {
                    console.warn('"action" takes a child flow');
                    this._childStack = [];
                } else {
                    this._childStack = childStack;
                }
                break;
            case "flow":
                if (!this._validateInstructionType("flow", instruction)) {
                    throw Error(`Invalid instruction category: "${instruction}" is not a flow`);
                }
                if (args === undefined) {
                    throw Error(`Invalid arguments: "${instruction}" requires arguments`);
                } else {
                    try {
                        this._args = this._validateArgs(instruction, args);
                    } catch (e) {
                        throw e;
                    }
                }
                if (childStack !== undefined) {
                    console.warn(`"${instruction}" takes no child flow`);
                }
                this._childStack = null;
                break;
            case "flow-no-args":
                if (!this._validateInstructionType("flow", instruction)) {
                    throw Error(`Invalid instruction category: "${instruction}" is not a flow`);
                }
                if (args !== undefined || childStack !== undefined) {
                    console.warn(`"${instruction}" takes no arguments or child flow`);
                }
                this._args = this._childStack = null;
                break;
            case "clamp":
                if (!this._validateInstructionType("clamp", instruction)) {
                    throw Error(`Invalid instruction category: "${instruction}" is not a clamp`);
                }
                if (args === undefined) {
                    throw Error(`Invalid arguments: "${instruction}" requires arguments`);
                } else {
                    try {
                        this._args = this._validateArgs(instruction, args);
                    } catch (e) {
                        throw e;
                    }
                }
                if (childStack === undefined) {
                    console.warn(`"${instruction}" takes a child flow`);
                    this._childStack = [];
                } else {
                    this._childStack = childStack;
                }
                break;
            case "clamp-no-args":
                if (!this._validateInstructionType("clamp", instruction)) {
                    throw Error(`Invalid instruction category: "${instruction}" is not a clamp`);
                }
                if (args !== undefined) {
                    console.warn(`"${instruction}" takes no arguments`);
                }
                this._args = null;
                if (childStack === undefined) {
                    console.warn(`"${instruction}" takes a child flow`);
                    this._childStack = [];
                } else {
                    this._childStack = childStack;
                }
                break;
            default:
                throw Error(`Invalid instruction type: "${type}" instruction doesn't exist`);
        }

        this._type = type;
    }

    private _validateInstructionType(type: TInstructionType, instruction: string): boolean {
        return true;
    }

    private _validateArgs(instruction: string, args: IArgElement[]): IArgElement[] {
        // throw Error(`Invalid arguments: .....`);
        return args;
    }

    /** Returns the instruction category. */
    get type() {
        return this._type;
    }

    /** Returns the state properties of the instruction. */
    get props() {
        const propObj: IInstructionProps = { instruction: this._instruction };
        if (this._args) {
            propObj["args"] = this._args;
        }
        if (this._childStack) {
            propObj["childStack"] = this._childStack;
        }
        return propObj;
    }
}

// ---- Abstract Syntax Tree (AST) -----------------------------------------------------------------

class AST implements IAST {
    /** Stores the singleton instance (once instantiated). */
    private static _instance: AST | undefined;

    private _startStacks: IStack[] = [];
    private _actionStacks: IStack[] = [];

    /** Creates and returns a new instance of the class if one doesn't exist, else returns the existing one. */
    constructor() {
        if (AST._instance) {
            return AST._instance;
        }
        AST._instance = this;
    }

    /** Getter that returns the singleton instance. */
    static get instance() {
        return AST._instance;
    }

    get startStacks() {
        return this._startStacks;
    }

    get actionStacks() {
        return this._actionStacks;
    }
}
