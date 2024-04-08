from dash import html

def paperWrapperComponent(dom):
    return html.Div(
        [dom],
        className="w-full h-full flex flex-col justify-center items-center p-0 bg-slate-800 rounded-lg shadow-lg hover:shadow-2xl",
    )

def timelineNode(title, top):
    """Create a node on top-{%val} of the timeline.

    Args:
        title (str): title of the node in middle.
        top (str): percentage/px for CSS top.

    Returns:
        _type_: _description_
    """
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        className=" w-[20px] h-[20px] md:w-8 md:h-8 border-t-[3px] border-l-[3px] border-slate-500"
                    ),
                    html.Div(
                        className="repeat-animation scroll-item-animate w-[20px] h-[20px] md:w-8 md:h-8 border-t-[3px] border-r-[3px] border-slate-500 need-animate-600 need-animate-delay-200 need-animate-slide-in-x-and-y hover:scale(1.05) hover:border-slate-400 transition duration-300 ease-in-out animate-slide-in-x-and-y animate-700 animate-delay-400"  # animate-slide-in-x-and-y animate-500 animate-delay-700
                    ),
                ],
                className="w-full flex flex-row justify-between items-start",
            ),
            html.H3(
                title,
                className="absolute top-1/2 left-1/2 text-slate-400 flex-1 font-semibold text-md md:text-3xl -rotate-45 text-center self-center select-none hover:text-slate-300 transition duration-500 ease-in-out translate-x-[-50%] translate-y-[-50%]",
            ),
            html.Div(
                [
                    html.Div(
                        className=" w-[20px] h-[20px] md:w-8 md:h-8 self-end border-b-[3px] border-r-[3px] border-slate-500"
                    ),
                ],
                className="w-full flex flex-row-reverse justify-between items-end",
            ),
        ],
        #! this container need animation at first place because it is the first item
        className=f"scroll-item-container absolute top-[{top}] left-[2rem] md:left-[5rem] w-14 h-14 md:w-28 md:h-28 lg:w-44 lg:h-44 bg-slate-900 rotate-45 translate-x-[-50%] translate-y-[-50%] flex flex-col justify-between",
    )

