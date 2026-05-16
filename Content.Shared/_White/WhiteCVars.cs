using Robust.Shared.Configuration;

namespace Content.Shared._White;

/*
 * PUT YOUR CUSTOM VARS HERE
 * DO IT OR I WILL KILL YOU
 * with love, by hailrakes
 */


[CVarDefs]
public sealed class WhiteCVars
{
    /*
   * NonPeaceful Round End
     */

    public static readonly CVarDef<bool> NonPeacefulRoundEndEnabled =
        CVarDef.Create("white.non_peaceful_round_end_enabled", true, CVar.SERVERONLY | CVar.ARCHIVE);

}
