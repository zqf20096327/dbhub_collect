# go-tidbits

## 10/9/2019
- When running `go get` on a project that uses `ldflags`, they won't be set. The application will have blank data. (e.g. version, build). Something to consider when using this functionality and suggesting users to get your project via `go get` instead of providing a binary produced through your build system.

- When running `go get` outside of the main module for an application (i.e. working directory is not in the modules path), `replace`/`exclude` directives do not apply. This can result in `go get` operations that fail to compile if the module takes the liberty of replacing and excluding certain dependencies.

## 10/10/2019
- Go 1.13 introduced the `-trimpath` argument which can assist in creating reproducible builds. When an error occurs, the stack trace has information relating to the build environment, this means a binary can be different based on where its built from. `-trimpath` removes these paths and only uses the module path.

## 10/11/2019
- When resolving whether or not a type satisfies an interface, if the type has a `pointer` receiver, if you create that type as a value type, the type will not satisfy the interface. However, if the type has a `value` receiver, then creating that type as a pointer _or_ value will satisfy the interface.

This is typically known as the _method set_ of a type.

```go
type Fooer interface {
	Foo()
}

type A struct { }

func (a A) Foo() { }

type B struct { }

func (b *B) Foo() { }

func main() {

	aVal := A{}
	aPtr := &A{}
	
	bVal := B{}
	
	var f Fooer
	
	f = aVal
	f = aPtr
    
    // This fails to compile because bVal was constructed
    // as a value type. It's receiver is a pointer type.
    // Thus, the interface is not satisfied.
	f = bVal

	
	fmt.Println(f)
}
```

- With embeded types, the embeded types semantic (i.e. pointer or value), takes precedences over the parent semantic. 

```go
    // Even though Admin is using value semantics, User will still use pointer.
    // If User is embedded into Admin, methods on User are still pointer semantics. TYPE LIFE.
	admin := Admin{
		User: &User{
			Name:  "john smith",
			Email: "john@email.com",
		},
		Level: "super",
    }
```

- When embedding types, if methods collide, the parent method takes precedence.

## 10/16/2019

- When checking if an error is a specific type, value and pointer semantics still matter. e.g. 

If the API you're using uses Value semantics for an error, you must use the same type when using errors.As() from 1.13. A lot of example tutorials say

```go
var e *MyError
errors.As(err, &e)
```

This fails if MyError uses value semantics from the API, i.e.

```go
return MyError{}
```

Because `MyError` is of type `MyError`, not `*MyError`

## Other Fun Facts Unrelated to Go

### Docker

- When using the `--target` argument, you can target a specific build step to be built in a Dockerfile. However, the `FROM` layers above will still be built, even if the `target` has no dependency on it.
